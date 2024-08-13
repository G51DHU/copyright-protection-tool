import os
import time
import json
import asyncio
import aiohttp
from aiohttp import ClientSession
from asyncio import Semaphore
from typing import Dict, List, Any, Optional
import logging

from exceptions import IndexerError

async def fetch_with_retries(session: ClientSession, semaphore: Semaphore, url: str, logger: logging.Logger, max_retries: int = 3) -> Optional[str]:
    for attempt in range(max_retries):
        try:
            async with semaphore, session.get(url) as response:
                response.raise_for_status()
                return await response.text()
        except aiohttp.ClientError as e:
            logger.error(f"Attempt {attempt + 1} failed: {str(e)}")
        
        await asyncio.sleep(2 ** attempt)  # Exponential backoff
    
    return None

async def process_page(session: ClientSession, semaphore: Semaphore, url: str, logger: logging.Logger) -> List[Dict[str, Any]]:
    # Implement page processing logic here
    # This function should fetch a page and extract basic information about items (e.g., movies, books, etc.)
    pass

async def process_item_details(session: ClientSession, semaphore: Semaphore, item: Dict[str, Any], logger: logging.Logger) -> Optional[Dict[str, Any]]:
    # Implement item detail processing logic here
    # This function should fetch and process detailed information about a single item
    pass

async def main(base_url: str, max_retries: int, output_dir: str, concurrency_limit: int, logger: logging.Logger) -> None:
    start_time = time.time()
    logger.info(f"Starting main function with base_url: {base_url}")

    async with aiohttp.ClientSession() as session:
        semaphore = Semaphore(concurrency_limit)

        # Fetch and process the first page to get total number of pages
        first_page = await fetch_with_retries(session, semaphore, base_url, logger, max_retries)
        if not first_page:
            raise IndexerError("Failed to fetch the first page after multiple attempts. Exiting.")

        # Extract total number of pages logic here
        total_pages = 1  # Replace with actual logic to determine total pages

        # Process all pages
        tasks = [process_page(session, semaphore, f"{base_url}?page={page}", logger) for page in range(1, total_pages + 1)]
        all_items = await asyncio.gather(*tasks)
        all_items = [item for page in all_items for item in page]

        logger.info(f"Total items extracted: {len(all_items)}")

        # Process item details
        detailed_items = []
        batch_size = 50
        for i in range(0, len(all_items), batch_size):
            batch = all_items[i:i+batch_size]
            tasks = [process_item_details(session, semaphore, item, logger) for item in batch]
            batch_results = await asyncio.gather(*tasks)
            detailed_items.extend([result for result in batch_results if result is not None])
            logger.info(f"Processed batch {i//batch_size + 1}/{(len(all_items) + batch_size - 1)//batch_size}")

        # Save results
        output_file = os.path.join(output_dir, "indexer_results.json")
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(detailed_items, f, ensure_ascii=False, indent=4)

        elapsed_time = time.time() - start_time
        logger.info(f"Completed processing {total_pages} pages and {len(detailed_items)} detailed items in {elapsed_time:.2f} seconds")

async def handler(settings: Dict[str, Any], logger: logging.Logger) -> None:
    logger.info("Handler function called")
    base_url = settings["base_url"]
    max_retries = settings["max_retries"]
    output_dir = os.path.abspath(settings["output_dir"])
    concurrency_limit = settings.get("concurrency_limit", 10)
    
    logger.info(f"Initializing with: max_retries={max_retries}, output_dir={output_dir}, concurrency_limit={concurrency_limit}")
    
    try:
        await main(base_url, max_retries, output_dir, concurrency_limit, logger)
        logger.info("Handler function completed successfully")
    except IndexerError as e:
        logger.error(f"Indexer error in handler: {str(e)}")
    except Exception as e:
        logger.error(f"Unexpected error in handler: {str(e)}")

# The following code allows the script to be run standalone for testing
if __name__ == "__main__":
    import sys
    import json

    if len(sys.argv) != 2:
        print("Usage: python indexer_template.py <path_to_settings_json>")
        sys.exit(1)

    with open(sys.argv[1], 'r') as f:
        settings = json.load(f)

    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)

    asyncio.run(handler(settings, logger))