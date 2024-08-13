"""
Configuration validation module for the indexer application.

This module provides functions to validate various configuration settings
used by the indexer application.
"""

import logging
from typing import Dict, Any
import validate
from urllib.parse import urlparse

class ConfigValidationError(Exception):
    """Custom exception for configuration validation errors."""
    pass

async def config(config_dict: Dict[str, Any]) -> None:
    """
    Validate all configuration settings.

    This function calls individual validation functions for each configuration section.
    If any validation fails, it raises a ConfigValidationError.

    Args:
        config_dict (Dict[str, Any]): The configuration dictionary to validate.

    Raises:
        ConfigValidationError: If any configuration setting is invalid.
    """
    try:
        validate_debug_level(config_dict)
        validate_path(config_dict, "path_for_list_of_supported_indexes", str)
        validate_fetch_concurrency_limit(config_dict)
        await validate_flaresolverr(config_dict)
        validate_path(config_dict, "output_dir", str)
        validate_max_retries(config_dict)
    except ConfigValidationError as e:
        logging.critical(f"Configuration validation failed: {str(e)}")
        raise

def validate_debug_level(config_dict: Dict[str, Any]) -> None:
    """
    Validate the debug level setting.

    Ensures the debug level is an integer between 0 and 4.

    Args:
        config_dict (Dict[str, Any]): The configuration dictionary.

    Raises:
        ConfigValidationError: If the debug level is invalid.
    """
    debug_level = config_dict.get("debug_level")
    if not isinstance(debug_level, int) or debug_level not in range(5):
        raise ConfigValidationError("Invalid 'debug_level'. Must be an integer between 0 and 4.")

def validate_path(config_dict: Dict[str, Any], key: str, expected_type: type) -> None:
    """
    Validate a path configuration setting.

    Ensures the specified path exists and is of the expected type.

    Args:
        config_dict (Dict[str, Any]): The configuration dictionary.
        key (str): The key in the configuration dictionary for the path.
        expected_type (type): The expected type of the path value.

    Raises:
        ConfigValidationError: If the path is invalid or of the wrong type.
    """
    value = config_dict.get(key)
    if not isinstance(value, expected_type):
        raise ConfigValidationError(f"'{key}' must be of type '{expected_type.__name__}'.")

def validate_fetch_concurrency_limit(config_dict: Dict[str, Any]) -> None:
    """
    Validate the fetch concurrency limit settings.

    Ensures the fetch concurrency limit is properly configured.

    Args:
        config_dict (Dict[str, Any]): The configuration dictionary.

    Raises:
        ConfigValidationError: If the fetch concurrency limit configuration is invalid.
    """
    fcl = config_dict.get("fetch_concurrency_limit", {})
    if not isinstance(fcl, dict):
        raise ConfigValidationError("'fetch_concurrency_limit' must be a dictionary.")
    
    if fcl.get("use_as_global_max_concurrency_value", False):
        if not isinstance(fcl.get("count"), int):
            raise ConfigValidationError("'fetch_concurrency_limit.count' must be an integer when 'use_as_global_max_concurrency_value' is True.")

async def validate_flaresolverr(config_dict: Dict[str, Any]) -> None:
    """
    Validate the FlareSolverr configuration.

    Ensures the FlareSolverr URL is valid and the concurrency limit is properly set.

    Args:
        config_dict (Dict[str, Any]): The configuration dictionary.

    Raises:
        ConfigValidationError: If the FlareSolverr configuration is invalid.
    """
    flaresolverr = config_dict.get("flaresolverr", {})
    logging.info(f"FlareSolverr config: {flaresolverr}")
    
    if not isinstance(flaresolverr, dict):
        raise ConfigValidationError("'flaresolverr' must be a dictionary.")
    
    url = flaresolverr.get("url")
    logging.info(f"FlareSolverr URL: {url}")
    
    if not isinstance(url, str):
        raise ConfigValidationError("'flaresolverr.url' must be a string.")
    
    parsed_url = urlparse(url)
    if not all([parsed_url.scheme, parsed_url.netloc]):
        raise ConfigValidationError("'flaresolverr.url' must be a valid URL string.")
    
    is_valid_url = await validate.validate_url(url)
    logging.info(f"Is valid URL: {is_valid_url}")
    
    if not is_valid_url:
        raise ConfigValidationError("'flaresolverr.url' must be a valid URL string.")
    
    if not isinstance(flaresolverr.get("concurrency_limit"), int):
        raise ConfigValidationError("'flaresolverr.concurrency_limit' must be an integer.")

def validate_max_retries(config_dict: Dict[str, Any]) -> None:
    """
    Validate the maximum retries configuration.

    Ensures the maximum retries setting is properly configured.

    Args:
        config_dict (Dict[str, Any]): The configuration dictionary.

    Raises:
        ConfigValidationError: If the maximum retries configuration is invalid.
    """
    max_retries = config_dict.get("max_retries", {})
    if not isinstance(max_retries, dict):
        raise ConfigValidationError("'max_retries' must be a dictionary.")
    
    if max_retries.get("use_as_global_max_retry_value", False):
        if not isinstance(max_retries.get("count"), int):
            raise ConfigValidationError("'max_retries.count' must be an integer when 'use_as_global_max_retry_value' is True.")