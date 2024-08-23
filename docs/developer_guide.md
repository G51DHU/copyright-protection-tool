# Developer Guide

Welcome to the Developer Guide for the Copyright Protection Tool. This guide provides detailed information for developers who want to contribute to the project or create new indexers.

## Table of Contents

1. [Project Structure](#project-structure)
2. [Setting Up Development Environment](#setting-up-development-environment)
3. [Adding a New Indexer](#adding-a-new-indexer)
4. [Core Components](#core-components)
5. [Best Practices](#best-practices)
6. [Testing](#testing)
7. [Debugging](#debugging)
8. [Performance Optimization](#performance-optimization)
9. [Contributing](#contributing)

## Project Structure

```
COPYRIGHT-PROTECTION-TOOL
├── config/
│   ├── config.json
│   └── supported_indexes.json
├── docs/
├── indexers/
│   ├── init.py
│   ├── 1337x.py
│   ├── YTS.py
│   └── indexer_template/
│       ├── indexer_template_readme.md
│       └── indexer_template.py
├── logs/
├── output/
├── validate/
│   ├── init.py
│   ├── validate_config.py
│   └── validate_url.py
├── venv/
├── version.py
├── exceptions.py
├── main.py
├── README.md
└── requirements.txt
```

## Setting Up Development Environment

1. Clone the repository:

- `git clone https://github.com/G51DHU/copyright-protection-tool.git`
- `cd copyright-protection-tool`

2. Create and activate a virtual environment:

- `python -m venv venv`
- `source venv/bin/activate`  # On Windows use `venv\Scripts\activate`

3. Install dependencies:

- `pip install -r requirements.txt`

4. Install development dependencies:

- `pip install pytest mypy flake8 black`

5. Set up pre-commit hooks (optional but recommended):

- pip install pre-commit
- pre-commit install

## Adding a New Indexer

1. Copy the indexer template:

- `cp indexers/indexer_template/indexer_template.py indexers/new_site_indexer.py`

2. Implement the following key functions in your new indexer:

- `process_page`: Scrape a single page and return a list of items found.
- `process_item_details`: Fetch and process detailed information about a single item.
- Customize the `main` function as needed.

3. Example of `process_page` function:

- ```python
    async def process_page(session: ClientSession, semaphore: Semaphore, url: str, logger: logging.Logger) -> List[Dict[str, Any]]:
        html_content = await fetch_with_retries(session, semaphore, url, logger)
        if not html_content:
            return []
        
        items = []
        # Implement parsing logic here
        # Use BeautifulSoup or lxml for HTML parsing
        return items

    ```


4. Update config/supported_indexes.json with the configuration for your new indexer:

-   ```json
    {
        "NewSiteIndexer": {
            "base_url": "https://example.com/browse/",
            "script_settings": {
            "max_retries": 5,
            "worker_count": 10,
            "page_limit": 100
            }
        }
    }
    ```

5. Implement error handling and logging in your indexer.

## Core Components

### main.py

The entry point of the application. It handles:

- Loading configurations
- Setting up logging
- Initializing and running indexers

### validate/

Contains modules for validating configurations and URLs:

- `validate_config.py`: Validates the structure and content of configuration files.

- `validate_url.py`: Provides URL validation functionality.

### exceptions.py

Defines custom exceptions used throughout the project.

## Best Practices

1. Use type hints to improve code readability and catch type-related errors early.

2. Follow PEP 8 style guide for Python code.

3. Use asynchronous programming (asyncio) for I/O-bound operations.

4. Implement proper error handling and logging in all functions.

5. Use the provided `fetch_with_retries` function for reliable network requests.

6. Respect website robots.txt files and implement appropriate rate limiting.

7. Use the semaphore to control concurrency and avoid overwhelming target websites.

8. Write clear, self-documenting code with appropriate comments.

## Testing

1. Write unit tests for your indexer in the `tests/` directory.

2. Run tests using pytest: 
    `pytest tests/`

3. To test a specific indexer:
`python indexers/your_indexer.py path_to_test_settings.json`

4. Implement integration tests to ensure different components work together correctly.

## Debugging

1. Set the `debug_level` in `config.json` to 4 for maximum verbosity.

2. Use the Python debugger (pdb) or an IDE's debugging tools to step through the code.

3. Check the log files in the `logs/` directory for detailed execution information.

## Performance Optimization

1. Use profiling tools to identify performance bottlenecks:

`python -m cProfile -o output.prof main.py`

2. Analyze the profile with tools like snakeviz:

`snakeviz output.prof`

3. Optimize CPU-bound tasks by using multiprocessing.

4. Use connection pooling and keep-alive connections for HTTP requests.

5. Implement caching mechanisms for frequently accessed data.


## Contributing

1. Fork the repository on GitHub.

2. Create a new branch for your feature or bug fix.

3. Write clear, concise commit messages.

4. Include unit tests for new features or bug fixes.

5. Ensure all tests pass and the code adheres to the project's style guide.

6. Submit a pull request with a clear description of your changes.

For more information on contributing, please read our Contribution Guidelines.
Remember to always respect copyright laws and the terms of service of the websites you're indexing. This tool is for educational and research purposes only.

