# User Guide for Copyright Protection Tool

## Table of Contents

1. [Introduction](#introduction)
2. [Installation](#installation)
3. [Configuration](#configuration)
4. [Running the Tool](#running-the-tool)
5. [Understanding the Output](#understanding-the-output)
6. [Managing Indexers](#managing-indexers)
7. [Troubleshooting](#troubleshooting)
8. [Advanced Usage](#advanced-usage)
9. [Security Considerations](#security-considerations)
10. [Frequently Asked Questions](#frequently-asked-questions)

## Introduction

The Copyright Protection Tool is designed to index and monitor content across various web platforms to identify potential copyright infringements. This guide will walk you through the process of setting up, configuring, and using the tool effectively.

## Installation

1. Ensure you have Python 3.8 or higher installed on your system.

2. Clone the repository:

`git clone https://github.com/G51DHU/copyright-protection-tool.git`

`cd copyright-protection-tool`

3. Set up a virtual environment:

`python -m venv venv`

`source venv/bin/activate  # On Windows use venv\Scripts\activate`

4. Install the required dependencies:

`pip install -r requirements.txt`

## Configuration

1. Copy the example configuration files:

`cp config/config.example.json config/config.json`

`cp config/supported_indexes.example.json config/supported_indexes.json`

2. Edit `config/config.json` to set global options:
- Set `debug_level` (0-4) to control logging verbosity
- Configure `output_dir` and `logging_path`
- Adjust `fetch_concurrency_limit` and `max_retries` as needed

3. Edit `config/supported_indexes.json` to configure indexers:
- Add or remove indexers as required
- Set `base_url` and `script_settings` for each indexer

## Running the Tool

1. Ensure your virtual environment is activated.
2. Run the main script: `python main.py`

3. The tool will start processing the configured indexers and display progress in the console.

## Understanding the Output

- Scraped data is saved in the `output_dir` specified in `config.json`
- Each indexer creates its own JSON file (e.g., `yts.json`, `1337x.json`)
- Log files are stored in the `logging_path` directory

## Managing Indexers

- To add a new indexer, create a new Python file in the `indexers/` directory
- Implement the required functions: `process_page`, `process_item_details`, and `main`
- Add the new indexer configuration to `supported_indexes.json`

## Troubleshooting

- Check the log files in the `logging_path` directory for error messages
- Ensure all configuration files are valid JSON
- Verify that the target websites are accessible from your network
- If using FlareSolverr, make sure it's running and configured correctly

## Advanced Usage

- Use the `flaresolverr` configuration to bypass anti-bot protections
- Adjust `fetch_concurrency_limit` to optimize performance for your network conditions
- Implement custom post-processing scripts to analyze the scraped data

## Security Considerations

- Always use the tool responsibly and in compliance with applicable laws
- Do not share your configuration files, as they may contain sensitive information
- Regularly update the tool and its dependencies to patch security vulnerabilities
- Use a VPN or proxy if required by your use case

## Frequently Asked Questions

1. Q: How often should I run the tool?
A: The frequency depends on your specific needs and the rate of change of the indexed websites. Daily or weekly runs are common.

2. Q: Can I use the tool for commercial purposes?
A: The tool is provided for educational and research purposes. Consult with a legal professional for commercial use.

3. Q: How can I contribute to the project?
A: Check the CONTRIBUTING.md file in the repository for guidelines on how to contribute.

4. Q: What should I do if an indexer stops working?
A: Check if the website structure has changed, update the indexer code accordingly, and submit a pull request with the fix.

5. Q: Is it legal to use this tool?
A: The legality depends on how you use it. Always ensure you have the right to index and analyze the content in question.

Remember, this tool is for educational and research purposes only. Users are responsible for ensuring their use complies with all applicable laws and regulations.