# API Reference for Copyright Protection Tool

This document provides a reference for the main components and functions of the Copyright Protection Tool.

## Table of Contents

1. [Main Module](#main-module)
2. [Indexer Base Class](#indexer-base-class)
3. [Utility Functions](#utility-functions)
4. [Configuration Validation](#configuration-validation)
5. [Exception Classes](#exception-classes)

## Main Module

### `main.py`

#### `async def main(path_for_config: str) -> None`

The entry point of the application.

- Parameters:
 - `path_for_config` (str): Path to the configuration file.
- Returns: None

#### `def setup_logging(config: Dict[str, Any]) -> logging.Logger`

Sets up logging based on the configuration.

- Parameters:
 - `config` (Dict[str, Any]): The configuration dictionary.
- Returns: logging.Logger

#### `def get_config(path_for_config: str) -> Dict[str, Any]`

Loads and returns the configuration from a JSON file.

- Parameters:
 - `path_for_config` (str): Path to the configuration file.
- Returns: Dict[str, Any]

#### `def get_list_of_indexers(path_for_list_of_supported_indexes: str) -> Dict[str, Any]`

Loads and returns the list of supported indexers from a JSON file.

- Parameters:
 - `path_for_list_of_supported_indexes` (str): Path to the supported indexes file.
- Returns: Dict[str, Any]

## Indexer Base Class

### `class IndexerBase`

Base class for all indexers.

#### `async def handler(settings: Dict[str, Any], logger: logging.Logger) -> None`

The main handler for the indexer.

- Parameters:
 - `settings` (Dict[str, Any]): Indexer-specific settings.
 - `logger` (logging.Logger): Logger instance.
- Returns: None

#### `async def process_page(session: ClientSession, semaphore: Semaphore, url: str, logger: logging.Logger) -> List[Dict[str, Any]]`

Processes a single page of the indexer.

- Parameters:
 - `session` (ClientSession): aiohttp client session.
 - `semaphore` (Semaphore): Semaphore for concurrency control.
 - `url` (str): URL of the page to process.
 - `logger` (logging.Logger): Logger instance.
- Returns: List[Dict[str, Any]]

#### `async def process_item_details(session: ClientSession, semaphore: Semaphore, item: Dict[str, Any], logger: logging.Logger) -> Optional[Dict[str, Any]]`

Processes details of a single item.

- Parameters:
 - `session` (ClientSession): aiohttp client session.
 - `semaphore` (Semaphore): Semaphore for concurrency control.
 - `item` (Dict[str, Any]): Item to process.
 - `logger` (logging.Logger): Logger instance.
- Returns: Optional[Dict[str, Any]]

## Utility Functions

### `validate/validate_url.py`

#### `async def url(url: str) -> bool`

Validates a given URL.

- Parameters:
 - `url` (str): The URL to validate.
- Returns: bool

#### `async def validate_url_with_timeout(url: str, timeout: float = 5.0) -> Optional[bool]`

Validates a URL with a timeout.

- Parameters:
 - `url` (str): The URL to validate.
 - `timeout` (float): The maximum time to wait for validation.
- Returns: Optional[bool]

### `validate/validate_config.py`

#### `async def config(config_dict: Dict[str, Any]) -> None`

Validates all configuration settings.

- Parameters:
 - `config_dict` (Dict[str, Any]): The configuration dictionary to validate.
- Returns: None

## Configuration Validation

### `validate_debug_level(config_dict: Dict[str, Any]) -> None`

Validates the debug level setting.

- Parameters:
 - `config_dict` (Dict[str, Any]): The configuration dictionary.
- Returns: None

### `validate_path(config_dict: Dict[str, Any], key: str, expected_type: type) -> None`

Validates a path configuration setting.

- Parameters:
 - `config_dict` (Dict[str, Any]): The configuration dictionary.
 - `key` (str): The key in the configuration dictionary for the path.
 - `expected_type` (type): The expected type of the path value.
- Returns: None

## Exception Classes

### `class IndexerError(Exception)`

Base exception class for the indexer project.

### `class ConfigurationError(IndexerError)`

Exception raised for configuration-related errors.

### `class URLValidationError(IndexerError)`

Exception raised for URL validation errors.

