# Performance Optimization Guide for Copyright Protection Tool

This document provides guidelines and best practices for optimizing the performance of the Copyright Protection Tool.

## Table of Contents

1. [Concurrency Settings](#concurrency-settings)
2. [Network Optimization](#network-optimization)
3. [Memory Management](#memory-management)
4. [Indexer-Specific Optimizations](#indexer-specific-optimizations)
5. [Output and Storage](#output-and-storage)
6. [Monitoring and Profiling](#monitoring-and-profiling)

## Concurrency Settings

- Adjust the `fetch_concurrency_limit` in `config.json` to balance between speed and resource usage:
  ```json
  "fetch_concurrency_limit": {
    "use_as_global_max_concurrency_value": true,
    "count": 16
  }
  ```
- Increase `worker_count` for indexers that can handle higher concurrency:
  ```json
  "script_settings": {
    "worker_count": 50
  }
  ```
- Be cautious not to set concurrency too high, as it may overwhelm target servers or your own system.

## Network Optimization

- Use FlareSolverr only when necessary, as it can introduce additional latency.
- Implement connection pooling to reuse connections for multiple requests.
- Consider using a caching mechanism for frequently accessed data to reduce network requests.

## Memory Management

- Process data in chunks to avoid excessive memory usage:
  ```python
  chunk_size = 1000
  for i in range(0, len(all_items), chunk_size):
      chunk = all_items[i:i+chunk_size]
      process_chunk(chunk)
  ```
- Implement incremental processing and saving of results instead of keeping all data in memory.

## Indexer-Specific Optimizations

- Customize each indexer's settings based on the target website's structure and limitations:
  ```json
  "YTS": {
    "script_settings": {
      "page_limit": 50,
      "chunk_size": 1000
    }
  }
  ```
- Use efficient parsing methods (e.g., lxml for HTML parsing) in your indexer implementations.


## Monitoring and Profiling

- Use the logging system to track performance metrics:
  ```python
  logger.info(f"Processed {len(items)} items in {elapsed_time:.2f} seconds")
  ```
- Implement checkpoints to allow for resuming long-running tasks in case of interruptions.
- Use Python's `cProfile` module for detailed performance analysis:
  ```bash
  python -m cProfile -o output.prof main.py
  ```
  Then analyze the results with tools like snakeviz:
  ```bash
  snakeviz output.prof
  ```

Remember to balance performance optimizations with the respect for target websites' resources and any legal or ethical considerations. Always test thoroughly after making performance-related changes to ensure the tool's reliability and accuracy are maintained.
