# Configuration Guide for Copyright Protection Tool

## Table of Contents

1. [Introduction](#introduction)
2. [Global Configuration (config.json)](#global-configuration-configjson)
3. [Indexer Configuration (supported_indexes.json)](#indexer-configuration-supported_indexesjson)
4. [FlareSolverr Configuration](#flaresolverr-configuration)
5. [Configuration Examples](#configuration-examples)
6. [Best Practices](#best-practices)

## Introduction

This guide explains how to configure the Copyright Protection Tool using the `config.json` and `supported_indexes.json` files. Proper configuration is crucial for the tool's effective operation.

## Global Configuration (config.json)

The `config.json` file contains global settings for the tool. Here's a breakdown of the available options:

```json
{
 "debug_level": 1,
 "path_for_list_of_supported_indexes": "./config/supported_indexes.json",
 "fetch_concurrency_limit": {
   "use_as_global_max_concurrency_value": false,
   "count": 8
 },
 "flaresolverr": {
   "url": "http://localhost:8191/v1",
   "concurrency_limit": 8
 },
 "output_dir": "./output/",
 "logging_path": "./logs/",
 "max_retries": {
   "use_as_global_max_retry_value": false,
   "count": 5
 }
}
```

- `debug_level` : Integer from 0 to 4, controlling the verbosity of logging. 
  - 0: CRITICAL
  - 1: ERROR
  - 2: WARNING
  - 3: INFO
  - 4: DEBUG


- `path_for_list_of_supported_indexes`: Path to the `supported_indexes.json` file.
- `fetch_concurrency_limit`: Controls the number of concurrent requests.

  - `use_as_global_max_concurrency_value`: If true, uses this value for all indexers.
  - `count`: The maximum number of concurrent requests.


- `flaresolverr`: Configuration for FlareSolverr (used for bypassing anti-bot measures).
- `output_dir`: Directory where scraped data will be saved.
- `logging_path`: Directory for log files.
- `max_retries`: Controls the number of retry attempts for failed requests.
  - `use_as_global_max_retry_value`: If true, uses this value for all indexers.
  - `count`: The maximum number of retry attempts.



## Indexer Configuration (supported_indexes.json)
The `supported_indexes.json` file defines the configuration for each indexer. Here's an example structure:

```json
{
  "YTS": {
    "base_url": "https://yts.mx/api/v2/list_movies.json",
    "script_settings": {
      "max_retries": 5,
      "worker_count": 50,
      "page_limit": 50,
      "chunk_size": 1000
    }
  },
  "1337x": {
    "base_url": "https://www.1377x.to/movie-library/",
    "script_settings": {
      "max_retries": 5,
      "flaresolverr": true
    }
  }
}

```

Each indexer entry should include:

- `base_url`: The starting URL for the indexer.
- `script_settings`: Specific settings for the indexer script.

  - These can vary depending on the indexer's requirements.
  - Common settings include `max_retries`, `worker_count`, and `flaresolverr` (boolean indicating whether FlareSolverr is needed).



## FlareSolverr Configuration
If you're scraping websites with anti-bot protection, you may need to use FlareSolverr. To configure it:

1. Ensure FlareSolverr is running (see Installation Guide for setup instructions).

2. In `config.json`, set the FlareSolverr URL and concurrency limit:

```json
"flaresolverr": {
  "url": "http://localhost:8191/v1",
  "concurrency_limit": 8
}
```

3. In `supported_indexes.json`, set `"flaresolverr": true` for indexers that require it.

## Configuration Examples

### Basic config.json

```json
{
  "debug_level": 1,
  "output_dir": "./output/",
  "logging_path": "./logs/",
  "fetch_concurrency_limit": {
    "use_as_global_max_concurrency_value": true,
    "count": 8
  },
  "max_retries": {
    "use_as_global_max_retry_value": true,
    "count": 5
  }
}
```

### Example supported_indexes.json

```json
{
  "YTS": {
    "base_url": "https://yts.mx/api/v2/list_movies.json",
    "script_settings": {
      "worker_count": 50,
      "page_limit": 50,
      "chunk_size": 1000
    }
  },
  "1337x": {
    "base_url": "https://www.1377x.to/movie-library/",
    "script_settings": {
      "flaresolverr": true
    }
  }
}
```

## Best Practices

1. Start with lower concurrency limits and increase gradually to avoid overwhelming target websites.

2. Adjust `debug_level` to 3 or 4 when troubleshooting issues.

3. Regularly review and update indexer configurations as website structures may change.

4. Use FlareSolverr only when necessary, as it can slow down the scraping process.

5. Ensure your `output_dir` and `logging_path` have sufficient disk space for large datasets.

6. Regularly backup your configuration files, especially when making changes.

7. Use environment variables for sensitive information instead of hardcoding in configuration files.

8. Test your configuration thoroughly after making changes to ensure the tool functions as expected.

9. When adding new indexers, start with conservative settings and gradually optimize.

10. Use relative paths in your configuration to make the tool more portable.

