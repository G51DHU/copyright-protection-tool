import os
import time
import json
from lxml import etree
from io import StringIO
import asyncio
import aiohttp
from aiohttp import ClientSession
from asyncio import Semaphore
from typing import Dict, List, Any, Optional
import logging

from exceptions import IndexerError

class ResponseCache:
    def __init__(self):
        self.cache = {}

    async def get(self, url: str) -> Optional[str]:
        return self.cache.get(url)

    async def set(self, url: str, response: str) -> None:
        self.cache[url] = response

response_cache = ResponseCache()

async def check_flaresolverr(session: ClientSession, flaresolverr_url: str, logger: logging.Logger) -> bool:
    try:
        async with session.get(flaresolverr_url, timeout=30) as response:
            if response.status in [200, 405]:
                return True
            else:
                logger.error(f"FlareSolverr returned status code: {response.status}")
    except aiohttp.ClientConnectorError as e:
        logger.error(f"Connection error to FlareSolverr: {str(e)}")
    except asyncio.TimeoutError:
        logger.error("Timeout while connecting to FlareSolverr")
    except Exception as e:
        logger.error(f"Unexpected error checking FlareSolverr: {str(e)}")
    return False

async def fetch_with_flaresolverr(session: ClientSession, semaphore: Semaphore, url: str, flaresolverr_url: str, logger: logging.Logger) -> Optional[str]:
    async with semaphore:
        cached_response = await response_cache.get(url)
        if cached_response:
            return cached_response

        headers = {"Content-Type": "application/json"}
        data = {
            "cmd": "request.get",
            "url": url,
            "maxTimeout": 60000
        }

        try:
            async with session.post(flaresolverr_url, headers=headers, json=data, timeout=90) as response:
                result = await response.json()
                if result['status'] == 'ok':
                    html_content = result['solution']['response']
                    await response_cache.set(url, html_content)
                    return html_content
                else:
                    logger.error(f"FlareSolverr error for {url}: {result['message']}")
                    logger.debug(f"Full FlareSolverr response: {result}")
                    return None
        except asyncio.TimeoutError:
            logger.error(f"Timeout error while fetching {url}")
        except aiohttp.ClientError as e:
            logger.error(f"Client error while fetching {url}: {str(e)}")
        except json.JSONDecodeError:
            logger.error(f"JSON decode error for FlareSolverr response from {url}")
        except Exception as e:
            logger.error(f"Unexpected error while fetching {url}: {str(e)}")
        return None

async def fetch_with_retries(session: ClientSession, semaphore: Semaphore, url: str, flaresolverr_url: str, logger: logging.Logger, max_retries: int = 3) -> Optional[str]:
    for attempt in range(max_retries):
        try:
            result = await fetch_with_flaresolverr(session, semaphore, url, flaresolverr_url, logger)
            if result:
                return result
        except Exception as e:
            logger.error(f"Attempt {attempt + 1} failed: {str(e)}")
        
        await asyncio.sleep(2 ** attempt)  # Exponential backoff
    
    return None

async def process_library_page(session: ClientSession, semaphore: Semaphore, base_url: str, page: int, flaresolverr_url: str, logger: logging.Logger) -> List[Dict[str, Any]]:
    url = f"{base_url}{page}"
    html_content = await fetch_with_retries(session, semaphore, url, flaresolverr_url, logger)
    if html_content:
        return extract_movie_data_from_library(url, html_content, logger)
    return []

async def process_movie_details(session: ClientSession, semaphore: Semaphore, movie: Dict[str, Any], flaresolverr_url: str, logger: logging.Logger) -> Optional[Dict[str, Any]]:
    url = f"https://www.1377x.to{movie['link']}"
    logger.info(f"Processing movie details of link: {movie['link']}")
    html_content = await fetch_with_retries(session, semaphore, url, flaresolverr_url, logger)
    if html_content:
        return extract_movie_data(html_content, url, logger)
    return None

def extract_movie_data_from_library(url: str, html_content: str, logger: logging.Logger) -> List[Dict[str, Any]]:
    logger.info(f"Beginning extraction of movie data from HTML content of base url: {url}")
    tree = etree.parse(StringIO(html_content), etree.HTMLParser())
    content_element = tree.xpath("/html/body/main/div/div/div[2]/ul")
    
    if not content_element:
        logger.warning("No content element found in the HTML. Unable to extract movie data.")
        return []
    
    li_elements = content_element[0].findall("li")
    logger.info(f"Found {len(li_elements)} movie elements to process")

    movie_data = []
    for index, element in enumerate(li_elements, 1):
        logger.debug(f"Processing movie element {index}/{len(li_elements)}")
        try:
            name = element.xpath(".//div[@class='modal-header']//h3/a/text()")[0].strip()
            link = element.xpath(".//div[@class='modal-header']//h3/a/@href")[0]
            summary = element.xpath(".//div[@class='modal-body']//p/text()")[0].strip()
            categories = element.xpath(".//div[@class='category']/span/text()")
            rating_element = element.xpath(".//span[@class='rating']/i")[0]
            rating_percentage = rating_element.get('style').split(':')[1].strip().rstrip('%')
                
            movie_data.append({
                'name': name,
                'link': link,
                'summary': summary,
                'categories': categories,
                'rating_percentage': rating_percentage,
            })
            logger.debug(f"Successfully extracted data for movie: {name}")
        except IndexError as e:
            logger.error(f"Error extracting data from movie element {index}: {str(e)}")
        except Exception as e:
            logger.error(f"Unexpected error processing movie element {index}: {str(e)}")
    
    logger.info(f"Finished extracting data for {len(movie_data)} movies")
    return movie_data

def extract_movie_data(html_content: str, movie_page_link: str, logger: logging.Logger) -> Optional[Dict[str, Any]]:
    logger.info("Beginning extraction of movie data from HTML content")
    tree = etree.parse(StringIO(html_content), etree.HTMLParser())
    
    try:
        title_elements = tree.xpath("//div[@class='torrent-detail-info']//h3/a/text()")
        title = title_elements[0].strip() if title_elements else "Unknown Title"
        logger.info(f"Extracted movie title: {title}")
        
        description_elements = tree.xpath("//div[@class='torrent-detail-info']//p/text()")
        description = description_elements[0].strip() if description_elements else "No description available"
        logger.info(f"Extracted movie description: {description}")
        
        categories = tree.xpath("//div[@class='torrent-category clearfix']/span/text()")
        logger.info(f"Extracted categories: {categories}")
        
        tr_elements = tree.xpath("//table[@class='table-list table table-responsive table-striped']/tbody/tr")
        
        if not tr_elements:
            logger.warning("No torrent elements found in the HTML. Unable to extract torrent data.")
            return None
        
        logger.info(f"Found {len(tr_elements)} torrent elements to process")

        torrents = []
        for index, element in enumerate(tr_elements, 1):
            logger.debug(f"Processing torrent element {index}/{len(tr_elements)}")
            try:
                name_element = element.xpath(".//td[@class='coll-1 name']/a[2]")
                name = name_element[0].text if name_element else "Unknown Name"
                link = name_element[0].get('href') if name_element else ""
                category_element = element.xpath(".//td[@class='coll-1 name']/a[1]/@href")
                category = category_element[0].split('/')[-3] if category_element else "Unknown Category"
                seeds = element.xpath(".//td[@class='coll-2 seeds']/text()")[0] if element.xpath(".//td[@class='coll-2 seeds']/text()") else "0"
                leeches = element.xpath(".//td[@class='coll-3 leeches']/text()")[0] if element.xpath(".//td[@class='coll-3 leeches']/text()") else "0"
                date = element.xpath(".//td[@class='coll-date']/text()")[0] if element.xpath(".//td[@class='coll-date']/text()") else "Unknown Date"
                size = element.xpath(".//td[@class='coll-4 size mob-uploader']/text()")[0] if element.xpath(".//td[@class='coll-4 size mob-uploader']/text()") else "Unknown Size"
                uploader_element = element.xpath(".//td[@class='coll-5 uploader']/a/text()")
                uploader = uploader_element[0] if uploader_element else "Unknown Uploader"
                
                torrents.append({
                    'name': name,
                    'link': link,
                    'subcategory': category,
                    'seeds': int(seeds) if seeds.isdigit() else 0,
                    'leeches': int(leeches) if leeches.isdigit() else 0,
                    'date': date,
                    'size': size,
                    'uploader': uploader
                })
                logger.debug(f"Successfully extracted data for torrent: {name}")
            except IndexError as e:
                logger.error(f"Error extracting data from torrent element {index}: {str(e)}")
            except Exception as e:
                logger.error(f"Unexpected error processing torrent element {index}: {str(e)}")
        
        movie_data = {
            'title': title,
            'summary': description,
            'categories': categories,
            'movie_page': movie_page_link,
            'torrents': torrents
        }
        
        logger.info(f"Finished extracting data for movie with {len(torrents)} torrents")
        return movie_data
    except Exception as e:
        logger.error(f"An unexpected error occurred while extracting movie data: {str(e)}")
        return None

async def main(base_url: str, max_retries: Dict[str, Any], output_dir: str, flaresolverr_url: str, concurrency_limit: int, logger: logging.Logger) -> None:
    start_time = time.time()
    logger.info(f"Starting main function with base_url: {base_url}")

    # Extract the actual retry count from the max_retries dictionary
    retry_count = max_retries.get('count', 5)  # Default to 5 if 'count' is not present

    async with aiohttp.ClientSession() as session:
        semaphore = Semaphore(concurrency_limit)

        if not await check_flaresolverr(session, flaresolverr_url, logger):
            raise IndexerError("FlareSolverr is not available. Please ensure it's running.")

        first_page = await fetch_with_retries(session, semaphore, base_url+"1", flaresolverr_url, logger, retry_count)
        if not first_page:
            raise IndexerError("Failed to fetch the first page after multiple attempts. Exiting.")

        tree = etree.parse(StringIO(first_page), etree.HTMLParser())
        last_page_elements = tree.xpath("/html/body/main/div/div/div[3]/ul/li[last()]/a")
        if not last_page_elements:
            raise IndexerError("Could not find the last page number. Exiting.")

        last_page_number = int(last_page_elements[0].text)
        logger.info(f"Total number of pages to process: {last_page_number}")

        tasks = [process_library_page(session, semaphore, base_url, page, flaresolverr_url, logger) for page in range(1, last_page_number + 1)]
        all_movie_data = await asyncio.gather(*tasks)
        all_movie_data = [movie for page in all_movie_data for movie in page]

        logger.info(f"Total movies extracted: {len(all_movie_data)}")

        complete_movie_data = []
        batch_size = 50
        for i in range(0, len(all_movie_data), batch_size):
            batch = all_movie_data[i:i+batch_size]
            tasks = [process_movie_details(session, semaphore, movie, flaresolverr_url, logger) for movie in batch]
            batch_results = await asyncio.gather(*tasks)
            complete_movie_data.extend([result for result in batch_results if result is not None])
            logger.info(f"Processed batch {i//batch_size + 1}/{(len(all_movie_data) + batch_size - 1)//batch_size}")

        output_file = os.path.join(output_dir, "one_three_three_seven_x.json")
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(complete_movie_data, f, ensure_ascii=False, indent=4)

        elapsed_time = time.time() - start_time
        logger.info(f"Completed processing {last_page_number} pages and {len(complete_movie_data)} detailed movie data in {elapsed_time:.2f} seconds")
        
async def handler(settings: Dict[str, Any], logger: logging.Logger) -> None:
    logger.info("Handler function called")
    base_url = settings["base_url"]
    max_retries = settings["max_retries"]  # This should be a dictionary
    output_dir = os.path.abspath(settings["output_dir"])
    flaresolverr_url = settings.get("flaresolverr_url", "http://localhost:8191/v1")
    concurrency_limit = settings.get("flaresolverr_concurrency_limit", 8)
    
    logger.info(f"Initializing with: max_retries={max_retries}, output_dir={output_dir}, flaresolverr_url={flaresolverr_url}, concurrency_limit={concurrency_limit}")
    
    try:
        await main(base_url, max_retries, output_dir, flaresolverr_url, concurrency_limit, logger)
        logger.info("Handler function completed successfully")
    except IndexerError as e:
        logger.error(f"Indexer error in 1337x handler: {str(e)}")
    except Exception as e:
        logger.error(f"Unexpected error in 1337x handler: {str(e)}")