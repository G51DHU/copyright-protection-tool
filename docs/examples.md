# Examples of Using the Copyright Protection Tool

This document provides examples of how to use the Copyright Protection Tool for various scenarios.

## Table of Contents

1. [Basic Usage](#basic-usage)
2. [Configuring Multiple Indexers](#configuring-multiple-indexers)
3. [Using FlareSolverr](#using-flaresolverr)
4. [Customizing Output](#customizing-output)
5. [Handling Large Datasets](#handling-large-datasets)

## Basic Usage

To run the Copyright Protection Tool with default settings:

1. Ensure your configuration files are set up correctly.
2. Open a terminal and navigate to the project directory.
3. Run the following command:

```bash
python main.py
```

This will start the tool with the default configuration, processing all configured indexers.

## Configuring Multiple Indexers

To use multiple indexers, update your `supported_indexes.json` file. Here's an example configuration for two indexers:

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

With this configuration, the tool will process both the YTS and 1337x indexers.

## Using FlareSolverr

To use FlareSolverr for bypassing anti-bot protections:

1. Ensure FlareSolverr is running (see Installation Guide).
2. In your `config.json`, set up FlareSolverr:

```json
{
  "flaresolverr": {
    "url": "http://localhost:8191/v1",
    "concurrency_limit": 8
  }
}
```

3. In your `supported_indexes.json`, enable FlareSolverr for the indexer:

```json
{
  "ProtectedSite": {
    "base_url": "https://protected-site.com/",
    "script_settings": {
      "flaresolverr": true
    }
  }
}
```

## Customizing Output

To customize the output directory:

1. In your `config.json`, set the `output_dir`:

```json
{
  "output_dir": "./custom_output/"
}
```

2. Run the tool as usual. The results will be saved in the specified directory.

## Handling Large Datasets

For processing large datasets:

1. Adjust the concurrency settings in `config.json`:

```json
{
  "fetch_concurrency_limit": {
    "use_as_global_max_concurrency_value": true,
    "count": 16
  }
}
```

2. Increase the `worker_count` in your indexer settings:

```json
{
  "LargeDataIndexer": {
    "base_url": "https://large-data-site.com/",
    "script_settings": {
      "worker_count": 100,
      "chunk_size": 5000
    }
  }
}
```

3. Run the tool. It will process the large dataset with increased parallelism.

Remember to adjust these settings carefully to avoid overwhelming the target websites or your local system resources.
