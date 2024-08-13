# Copyright Protection Tool - Project Overview

## Introduction

The Copyright Protection Tool is a sophisticated system designed to index and monitor content across various web platforms, with a primary focus on identifying potential copyright infringements. This tool employs web scraping techniques to gather data from multiple sources, process it, and store the results for further analysis.

## Table of Contents

1. [Project Structure](#project-structure)
2. [Key Components](#key-components)
3. [Installation](#installation)
4. [Usage](#usage)
5. [Workflow](#workflow)
6. [Adding New Indexers](#adding-new-indexers)
7. [Error Handling and Logging](#error-handling-and-logging)
8. [Configuration](#configuration)
9. [Contributing](#contributing)
10. [License](#license)

## Project Structure

The project is organized into several key directories and files:

```
copyright-protection-tool/
│
├── config/
│   ├── config.json
│   └── supported_indexes.json
│
├── indexers/
│   ├── __init__.py
│   │
│   ├── indexer_template/
│   │   ├── indexer_template
│   │   └── indexer_template_readme.md
│   │
│   ├── 1337x.py
│   └── YTS.py
│
├── logs/
│   └── main.log
│
├── output/
│
├── validate/
│   ├── __init__.py
│   ├── validate_config.py
│   └── validate_url.py
│
├── venv/
│
├── exceptions.py
├── main.py
└── english_public_trackers.json
```

## Key Components

### 1. Configuration (`config/`)
- `config.json`: Contains global settings for the tool.
- `supported_indexes.json`: Defines the indexers and their specific configurations.

### 2. Indexers (`indexers/`)
- `indexer_template.py`: A template for creating new indexers.
- `indexer_template_readme.md`: Detailed documentation on how to use the indexer template and create new indexers.
- Individual indexer files (e.g., `1337x.py`, `YTS.py`): Implement specific scraping logic for different websites.

### 3. Validation (`validate/`)
- `validate_config.py`: Ensures the configuration files are correctly structured and contain valid data.
- `validate_url.py`: Provides URL validation functionality.

### 4. Main Execution (`main.py`)
- Serves as the entry point for the application.
- Orchestrates the overall execution flow, including configuration loading, indexer initialization, and execution.

### 5. Exception Handling (`exceptions.py`)
- Defines custom exceptions for the project to handle various error scenarios.

### 6. Logging (`logs/`)
- Stores log files to track the application's execution and any issues that arise.

### 7. Output (`output/`)
- Destination for the processed data and results from the indexers.

## Installation

To set up the Copyright Protection Tool, follow these steps:

1. Clone the repository:
   ```
   git clone https://github.com/your-username/copyright-protection-tool.git
   cd copyright-protection-tool
   ```

2. Create a virtual environment:
   ```
   python -m venv venv
   ```

3. Activate the virtual environment:
   - On Windows: `venv\Scripts\activate`
   - On macOS and Linux: `source venv/bin/activate`

4. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

5. Configure the tool by editing `config/config.json` and `config/supported_indexes.json` as needed.

## Usage

To run the Copyright Protection Tool:

1. Ensure your virtual environment is activated.

2. Run the main script:
   ```
   python main.py
   ```

3. The tool will process each configured indexer and store the results in the `output/` directory.

4. Check the `logs/main.log` file for execution details and any errors.

## Workflow

1. The application starts by loading and validating the configuration from `config.json` and `supported_indexes.json`.
2. It then initializes the logger and sets up the execution environment.
3. For each configured indexer in `supported_indexes.json`:
   - The corresponding indexer module is dynamically loaded.
   - The indexer's `handler` function is called with the appropriate settings.
4. Each indexer performs its specific web scraping tasks:
   - Fetching web pages
   - Parsing content
   - Extracting relevant information
5. The extracted data is processed and stored in the `output/` directory.
6. Logs are continuously written to `logs/main.log` for monitoring and debugging.

## Adding New Indexers

To add support for a new website:
1. Refer to `indexers/indexer_template_readme.md` for detailed instructions on creating new indexers.
2. Create a new Python file in the `indexers/` directory using `indexer_template.py` as a base.
3. Implement the specific scraping logic for the new website.
4. Add the new indexer's configuration to `supported_indexes.json`.

The `indexer_template_readme.md` file provides comprehensive guidance on:
- Understanding the template structure
- Implementing required functions
- Best practices for indexer development
- Testing and troubleshooting new indexers

## Error Handling and Logging

The project uses a custom exception hierarchy defined in `exceptions.py` to handle various error scenarios. Comprehensive logging is implemented throughout the application to facilitate debugging and monitoring.

## Configuration

The `config.json` file allows for customization of various global settings, including:
- Debug levels
- Output and logging paths
- Concurrency limits
- FlareSolverr settings (for bypassing anti-bot measures)

## Contributing

We welcome contributions to the Copyright Protection Tool! Please see our [CONTRIBUTE.md](CONTRIBUTE.md) file for details on how to get started, and the process for submitting pull requests.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Conclusion

This Copyright Protection Tool provides a flexible and extensible framework for monitoring content across multiple web platforms. Its modular design, coupled with detailed documentation for indexer creation, allows for easy addition of new indexers and adaptation to changes in target websites. The combination of asynchronous processing, robust error handling, and comprehensive logging makes it a powerful tool for copyright monitoring and protection.