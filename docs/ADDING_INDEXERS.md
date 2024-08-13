# Adding New Indexers to the Copyright Protection Tool

This guide provides step-by-step instructions on how to add new indexers to the Copyright Protection Tool. By following these steps, you can extend the tool's capability to scrape and index content from additional websites.

## Table of Contents

1. [Overview](#overview)
2. [Prerequisites](#prerequisites)
3. [Step-by-Step Guide](#step-by-step-guide)
   - [1. Create a New Indexer File](#1-create-a-new-indexer-file)
   - [2. Implement Required Functions](#2-implement-required-functions)
   - [3. Customize the Main Function](#3-customize-the-main-function)
   - [4. Update Configuration Files](#4-update-configuration-files)
   - [5. Test Your New Indexer](#5-test-your-new-indexer)
4. [Best Practices](#best-practices)
5. [Troubleshooting](#troubleshooting)

## Overview

An indexer is a Python script that defines how to scrape and process data from a specific website. The Copyright Protection Tool uses a template-based approach to make adding new indexers as straightforward as possible.

## Prerequisites

Before adding a new indexer, ensure you have:

- Basic knowledge of Python programming
- Familiarity with web scraping concepts
- Understanding of the website you want to index
- The Copyright Protection Tool set up and running correctly

## Step-by-Step Guide

### 1. Create a New Indexer File

1. Navigate to the `indexers/` directory in your project.
2. Copy the `indexer_template.py` file and rename it to match your new indexer (e.g., `new_site_indexer.py`).

### 2. Implement Required Functions

Open your new indexer file and implement the following key functions:

#### a. `process_page`

This function should scrape a single page and return a list of items found on that page.

```python
async def process_page(session: ClientSession, semaphore: Semaphore, url: str, logger: logging.Logger) -> List[Dict[str, Any]]:
    html_content = await fetch_with_retries(session, semaphore, url, logger)
    if not html_content:
        return []
    
    # Parse HTML and extract items
    items = []
    # ... (implement parsing logic here)
    return items
```

#### b. `process_item_details`

This function should fetch and process detailed information about a single item.

```python
async def process_item_details(session: ClientSession, semaphore: Semaphore, item: Dict[str, Any], logger: logging.Logger) -> Optional[Dict[str, Any]]:
    url = item['detail_url']
    html_content = await fetch_with_retries(session, semaphore, url, logger)
    if not html_content:
        return None
    
    # Parse HTML and extract detailed information
    details = {}
    # ... (implement parsing logic here)
    return details
```

### 3. Customize the Main Function

Modify the `main` function to fit the structure of the website you're indexing. This may involve:

- Determining the total number of pages to scrape
- Adjusting the logic for processing pages and items
- Customizing how data is saved

### 4. Update Configuration Files

1. Open `config/supported_indexes.json`
2. Add a new entry for your indexer:

```json
{
  "NewSiteIndexer": {
    "base_url": "https://www.newsite.com/browse/",
    "script_settings": {
      "max_retries": 5,
      "worker_count": 10,
      "page_limit": 100
    }
  }
}
```

Adjust the settings as needed for your specific indexer.

### 5. Test Your New Indexer

1. Run the main script:
   ```
   python main.py
   ```
2. Check the console output and log files for any errors.
3. Verify that the data is being correctly scraped and saved in the `output/` directory.

## Best Practices

1. **Respect robots.txt**: Always check and respect the website's robots.txt file.
2. **Rate Limiting**: Implement appropriate delays between requests to avoid overwhelming the target website.
3. **Error Handling**: Implement robust error handling to deal with network issues, changes in website structure, etc.
4. **Logging**: Use the provided logger to record important information and potential issues.
5. **Code Comments**: Add clear comments to explain complex parts of your scraping logic.
6. **Modularity**: Break down complex scraping tasks into smaller, reusable functions.

## Troubleshooting

- If your indexer is not being recognized, ensure it's correctly added to `supported_indexes.json`.
- For parsing errors, double-check the website's HTML structure and update your parsing logic accordingly.
- If you encounter rate limiting or blocking, consider implementing delays or using FlareSolverr if necessary.
- Use the debug logging level to get more detailed information about the execution flow.

Remember to test your indexer thoroughly and ensure it can handle various edge cases and potential errors gracefully.

For more complex issues or questions, please refer to the project's issue tracker or reach out to the community for support.