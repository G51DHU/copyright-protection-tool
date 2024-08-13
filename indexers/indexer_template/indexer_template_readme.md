# Indexer Template Documentation

## Overview

The indexer template provides a standardized structure for creating new web scrapers (indexers) in the project. It offers a consistent interface and common functionality, allowing developers to focus on implementing the specific logic required for each new website to be indexed.

## File Structure

The template is located at `indexers/indexer_template.py`. When creating a new indexer, copy this file and rename it to match your new indexer (e.g., `new_website_indexer.py`).

## Components

### Imports

The template includes common imports required for asynchronous web scraping:

```python
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
```

Ensure all these dependencies are installed in your environment.

### Helper Functions

#### `fetch_with_retries`

```python
async def fetch_with_retries(session: ClientSession, semaphore: Semaphore, url: str, logger: logging.Logger, max_retries: int = 3) -> Optional[str]:
```

This function handles fetching a URL with retry logic. It uses exponential backoff to handle temporary failures.

### Main Processing Functions

#### `process_page`

```python
async def process_page(session: ClientSession, semaphore: Semaphore, url: str, logger: logging.Logger) -> List[Dict[str, Any]]:
```

This function should be implemented to process a single page of the website being indexed. It should return a list of dictionaries, each containing basic information about an item found on the page.

#### `process_item_details`

```python
async def process_item_details(session: ClientSession, semaphore: Semaphore, item: Dict[str, Any], logger: logging.Logger) -> Optional[Dict[str, Any]]:
```

This function should be implemented to fetch and process detailed information about a single item. It takes the basic item information and should return a dictionary with full details.

### Main Execution Function

#### `main`

```python
async def main(base_url: str, max_retries: int, output_dir: str, concurrency_limit: int, logger: logging.Logger) -> None:
```

This function orchestrates the entire indexing process. It fetches pages, processes items, and saves results. Customize this function as needed for your specific indexer.

### Handler Function

#### `handler`

```python
async def handler(settings: Dict[str, Any], logger: logging.Logger) -> None:
```

This is the entry point for the indexer. It takes settings and a logger as parameters and calls the `main` function with the appropriate arguments.

## Usage

To create a new indexer:

1. Copy `indexer_template.py` to a new file named after your indexer (e.g., `new_website_indexer.py`).
2. Implement the `process_page` and `process_item_details` functions according to the structure of the website you're indexing.
3. Modify the `main` function if necessary, especially the part where the total number of pages is determined.
4. Adjust any other parts of the template to fit the specific requirements of the new indexer.

### Implementing `process_page`

This function should:
- Fetch the HTML content of a page
- Parse the HTML to extract basic information about each item on the page
- Return a list of dictionaries, each containing the basic info of an item

Example:
```python
async def process_page(session: ClientSession, semaphore: Semaphore, url: str, logger: logging.Logger) -> List[Dict[str, Any]]:
    html_content = await fetch_with_retries(session, semaphore, url, logger)
    if not html_content:
        return []
    
    # Parse HTML and extract items
    items = []
    # ... (parsing logic here)
    return items
```

### Implementing `process_item_details`

This function should:
- Fetch the detailed page for an item
- Parse the HTML to extract all relevant information
- Return a dictionary with the full details of the item

Example:
```python
async def process_item_details(session: ClientSession, semaphore: Semaphore, item: Dict[str, Any], logger: logging.Logger) -> Optional[Dict[str, Any]]:
    url = item['detail_url']
    html_content = await fetch_with_retries(session, semaphore, url, logger)
    if not html_content:
        return None
    
    # Parse HTML and extract detailed information
    details = {}
    # ... (parsing logic here)
    return details
```

## Best Practices

1. Use the provided `fetch_with_retries` function to handle network requests reliably.
2. Implement proper error handling and logging throughout your indexer.
3. Respect the website's robots.txt file and implement appropriate rate limiting.
4. Use the semaphore to control concurrency and avoid overwhelming the target website.
5. Regularly test your indexer to ensure it adapts to any changes in the website's structure.

## Testing

The template includes a standalone execution block for testing:

```python
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
```

To test your indexer, create a JSON file with the necessary settings and run:

```
python new_website_indexer.py path_to_settings.json
```

Ensure your settings JSON includes all necessary parameters (base_url, max_retries, output_dir, etc.).