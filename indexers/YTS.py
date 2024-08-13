import os
import time
import requests
from concurrent.futures import ThreadPoolExecutor, as_completed
from multiprocessing import Pool, cpu_count
import io
import orjson as json
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry  # type: ignore
from typing import Dict, List, Any, Optional
import logging

from exceptions import IndexerError

def create_session(max_retries: int) -> requests.Session:
    session = requests.Session()
    retries = Retry(total=max_retries,
                    backoff_factor=0.1,
                    status_forcelist=[500, 502, 503, 504])
    session.mount('https://', HTTPAdapter(max_retries=retries))
    return session

def fetch_page(base_url: str, session: requests.Session, page: int, page_limit: int, logger: logging.Logger) -> Optional[Dict[str, Any]]:
    try:
        response = session.get(f"{base_url}?limit={page_limit}&page={page}", timeout=30)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        logger.error(f"Error fetching page {page}: {e}")
        return None

def worker(base_url: str, page: int, max_retries: int, page_limit: int, logger: logging.Logger) -> List[Dict[str, Any]]:
    session = create_session(max_retries)
    response = fetch_page(base_url, session, page, page_limit, logger)
    if response and 'data' in response and 'movies' in response['data']:
        logger.info(f"Successfully fetched page {page}")
        return response['data']['movies']
    logger.warning(f"No movies found on page {page}")
    return []

def json_dump_movie(movie: Dict[str, Any]) -> bytes:
    return json.dumps(movie)

def process_chunk(chunk: List[Dict[str, Any]]) -> List[bytes]:
    return [json_dump_movie(movie) for movie in chunk]

def write_chunk_to_file(file: io.BufferedWriter, chunk: List[bytes]) -> None:
    for movie_json in chunk:
        file.write(movie_json)
        file.write(b'\n')

async def main(base_url: str, max_retries: int, worker_count: int, page_limit: int, chunk_size: int, output_dir: str, logger: logging.Logger) -> None:
    start_time = time.time()

    session = create_session(max_retries)

    logger.info("Fetching first page to determine total movie count...")
    first_page = fetch_page(base_url, session, 1, page_limit, logger)
    if not first_page:
        raise IndexerError("Failed to fetch the first page. Exiting.")

    total_movies = first_page['data']['movie_count']
    total_pages = (total_movies + page_limit - 1) // page_limit

    logger.info(f"Total movies: {total_movies}, Total pages: {total_pages}")

    all_movies = []
    movie_count = 0

    with ThreadPoolExecutor(max_workers=worker_count) as executor:
        future_to_page = {executor.submit(worker, base_url, page, max_retries, page_limit, logger): page for page in range(1, total_pages + 1)}
        
        for future in as_completed(future_to_page):
            page = future_to_page[future]
            try:
                movies = future.result()
                all_movies.extend(movies)
                movie_count += len(movies)
                logger.info(f"Processed page {page}, total movies: {movie_count}")
            except Exception as e:
                logger.error(f"Error processing page {page}: {e}")

    logger.info(f"Fetched {movie_count} movies. Starting JSON serialization...")

    output_file = os.path.join(output_dir, "yts.json")

    with Pool(cpu_count()) as pool:
        with open(output_file, "wb") as f:
            writer = io.BufferedWriter(f, buffer_size=8*1024*1024) 
            
            for i in range(0, len(all_movies), chunk_size):
                chunk = all_movies[i:i+chunk_size]
                serialized_chunk = pool.apply(process_chunk, (chunk,))
                write_chunk_to_file(writer, serialized_chunk)
                logger.info(f"Processed and wrote chunk {i//chunk_size + 1}")
            
            writer.flush()

    elapsed_time = time.time() - start_time
    logger.info(f"Fetched and saved {movie_count} movies in {elapsed_time:.2f} seconds")
    
    file_size = os.path.getsize(output_file) / (1024 * 1024)  # Size in MB
    logger.info(f"Output file size: {file_size:.2f} MB")

async def handler(settings: Dict[str, Any], logger: logging.Logger) -> None:
    logger.info("Handler function called")
    logger.info(f"Settings: {settings}")
    base_url = settings["base_url"]
    max_retries = settings["max_retries"]
    worker_count = settings["worker_count"]
    page_limit = settings["page_limit"]
    chunk_size = settings["chunk_size"]
    output_dir = os.path.abspath(settings["output_dir"])

    try:
        await main(base_url, max_retries, worker_count, page_limit, chunk_size, output_dir, logger)
        logger.info("Handler function completed successfully")
    except IndexerError as e:
        logger.error(f"Indexer error in YTS handler: {str(e)}")
    except Exception as e:
        logger.error(f"Unexpected error in YTS handler: {str(e)}")