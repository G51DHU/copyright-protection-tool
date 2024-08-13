"""
URL validation module for the indexer application.

This module provides functions to validate URLs, including checks for
IP addresses and domain names.
"""

import re
import ipaddress
import asyncio
from urllib.parse import urlparse
from concurrent.futures import ThreadPoolExecutor
import logging
from typing import Optional

# Constants
ALLOWED_SCHEMES = {'http', 'https'}
MAX_URL_LENGTH = 2083  # Common limit used by browsers

# Simplified regex for domain labels
ALLOWED_CHARS = re.compile(r'^[a-z0-9]([a-z0-9-]{0,61}[a-z0-9])?$', re.IGNORECASE)

class URLValidationError(Exception):
    """Custom exception for URL validation errors."""
    pass

async def url(url: str) -> bool:
    """
    Validate a given URL.

    This function checks if the URL is valid by verifying its length,
    scheme, and whether it's an IP address or a valid domain name.

    Args:
        url (str): The URL to validate.

    Returns:
        bool: True if the URL is valid, False otherwise.

    Raises:
        URLValidationError: If there's an error during validation.
    """
    logging.info(f"Validating URL: {url}")
    
    if len(url) > MAX_URL_LENGTH:
        logging.info("URL exceeds maximum length")
        return False

    try:
        parsed = urlparse(url)
    except ValueError:
        logging.info("URL parsing failed")
        return False

    logging.info(f"Parsed URL: scheme={parsed.scheme}, netloc={parsed.netloc}, hostname={parsed.hostname}")

    if parsed.scheme not in ALLOWED_SCHEMES:
        logging.info(f"Invalid scheme: {parsed.scheme}")
        return False

    if not parsed.netloc:
        logging.info("No netloc in URL")
        return False

    host = parsed.hostname
    if not host:
        logging.info("No hostname in URL")
        return False

    try:
        # Use ThreadPoolExecutor for CPU-bound tasks
        with ThreadPoolExecutor() as executor:
            is_ip = await asyncio.get_event_loop().run_in_executor(
                executor, check_ip_address, host
            )
            if is_ip:
                logging.info("Valid IP address")
                return True

            is_valid_domain = await asyncio.get_event_loop().run_in_executor(
                executor, validate_domain, host
            )
            if not is_valid_domain:
                logging.info("Invalid domain")
                return False

        logging.info("URL validation successful")
        return True
    except Exception as e:
        raise URLValidationError(f"Error during URL validation: {str(e)}")

def check_ip_address(host: str) -> bool:
    """
    Check if the given host is a valid IP address.

    Args:
        host (str): The host to check.

    Returns:
        bool: True if the host is a valid IP address, False otherwise.
    """
    try:
        ipaddress.ip_address(host.strip('[]'))
        return True
    except ValueError:
        return False

def validate_domain(host: str) -> bool:
    """
    Validate a domain name.

    This function checks if the given host is a valid domain name
    by verifying its length and label format.

    Args:
        host (str): The domain name to validate.

    Returns:
        bool: True if the domain is valid, False otherwise.
    """
    logging.info(f"Validating domain: {host}")
    
    if host == 'localhost':
        logging.info("Valid localhost")
        return True
    
    if len(host) > 253:
        logging.info("Domain name too long")
        return False
    
    labels = host.split('.')
    if len(labels) < 2:
        logging.info("Not enough domain labels")
        return False
    
    for label in labels:
        if not ALLOWED_CHARS.match(label) or len(label) > 63:
            logging.info(f"Invalid domain label: {label}")
            return False
    
    logging.info("Valid domain")
    return True

async def validate_url_with_timeout(url: str, timeout: float = 5.0) -> Optional[bool]:
    """
    Validate a URL with a timeout.

    This function wraps the url validation function with a timeout
    to ensure the validation doesn't hang indefinitely.

    Args:
        url (str): The URL to validate.
        timeout (float): The maximum time (in seconds) to wait for validation.

    Returns:
        Optional[bool]: True if the URL is valid, False if invalid, 
                        None if validation timed out.

    Raises:
        URLValidationError: If there's an error during validation.
    """
    try:
        return await asyncio.wait_for(url(url), timeout=timeout)
    except asyncio.TimeoutError:
        logging.warning(f"URL validation timed out for: {url}")
        return None
    except URLValidationError as e:
        logging.error(f"URL validation error: {str(e)}")
        raise