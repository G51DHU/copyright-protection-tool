# Troubleshooting Guide for Copyright Protection Tool

This document provides solutions to common issues you may encounter while using the Copyright Protection Tool. If you're experiencing a problem not covered here, please check the project's issue tracker or reach out to the community for support.

## Table of Contents

1. [General Issues](#general-issues)
2. [Configuration Issues](#configuration-issues)
3. [Indexer-Specific Issues](#indexer-specific-issues)
4. [FlareSolverr Issues](#flaresolverr-issues)
5. [Performance Issues](#performance-issues)
6. [Output and Logging Issues](#output-and-logging-issues)
7. [Debugging Tips](#debugging-tips)

## General Issues

### The tool doesn't start

**Symptom**: When running `python main.py`, nothing happens or you get an immediate error.

**Possible solutions**:
1. Ensure you're in the correct directory and your virtual environment is activated.
2. Verify that all dependencies are installed: `pip install -r requirements.txt`
3. Check that you're using Python 3.8 or higher: `python --version`
4. Look for any error messages in the console output.

### ModuleNotFoundError

**Symptom**: You see an error like `ModuleNotFoundError: No module named 'some_module'`

**Solution**: Install the missing module using pip:
```
pip install some_module
```
If the module should be part of the project's dependencies, make sure you've run `pip install -r requirements.txt`.

## Configuration Issues

### ConfigurationError: "Invalid JSON in config file"

**Symptom**: The tool reports an invalid JSON error when starting.

**Solutions**:
1. Check your `config.json` and `supported_indexes.json` for syntax errors.
2. Ensure all required fields are present in both files.
3. Use a JSON validator tool to verify the structure of your JSON files.

### IndexerError: "Failed to fetch the first page after multiple attempts"

**Symptom**: The tool can't access the target website.

**Solutions**:
1. Check your internet connection.
2. Verify that the target website is accessible in your web browser.
3. If using FlareSolverr, ensure it's running and configured correctly.
4. Check if the website's structure or URL has changed recently.

## Indexer-Specific Issues

### Indexer not found

**Symptom**: You get an error saying an indexer couldn't be found.

**Solutions**:
1. Ensure the indexer is correctly added to `supported_indexes.json`.
2. Check that the indexer file exists in the `indexers/` directory and is named correctly.
3. Verify that the indexer file contains a `handler` function.

### Indexer returns no data

**Symptom**: The indexer runs without errors but doesn't return any data.

**Solutions**:
1. Check if the website's structure has changed and update your parsing logic.
2. Verify that you're using the correct CSS selectors or XPath expressions for data extraction.
3. Ensure you're not being blocked by the website (you might need to implement delays or use FlareSolverr).

## FlareSolverr Issues

### FlareSolverr connection failed

**Symptom**: You get an error about failing to connect to FlareSolverr.

**Solutions**:
1. Ensure FlareSolverr is running: `docker ps` should show the FlareSolverr container.
2. Check that the FlareSolverr URL in `config.json` is correct.
3. Verify that your firewall isn't blocking the connection to FlareSolverr.

### FlareSolverr returns errors

**Symptom**: FlareSolverr is running but returns error responses.

**Solutions**:
1. Check FlareSolverr logs for any specific error messages.
2. Ensure you're using a compatible version of FlareSolverr.
3. Try restarting the FlareSolverr container.

## Performance Issues

### Indexing is very slow

**Symptom**: The tool takes an unusually long time to process pages.

**Solutions**:
1. Adjust concurrency settings in your configuration to allow more parallel requests.
2. Check your network speed and stability.
3. Ensure you're not making too many requests too quickly (which might trigger rate limiting).
4. Consider using a more powerful machine for large indexing jobs.

### High memory usage

**Symptom**: The tool consumes a lot of memory, potentially causing your system to slow down.

**Solutions**:
1. Reduce the batch size for processing items.
2. Implement incremental saving of results instead of keeping everything in memory.
3. Close any unnecessary applications to free up system resources.

## Output and Logging Issues

### No output files generated

**Symptom**: The tool runs without errors, but no output files are created.

**Solutions**:
1. Check that the `output_dir` in `config.json` is set correctly and the directory exists.
2. Ensure the tool has write permissions for the output directory.
3. Verify that the indexer is actually finding and processing data (check log files).

### Log files not created

**Symptom**: No log files are being generated in the specified logging directory.

**Solutions**:
1. Verify that the `logging_path` in `config.json` is set correctly and the directory exists.
2. Ensure the tool has write permissions for the logging directory.
3. Check that the `debug_level` in `config.json` is set to an appropriate level (1-4).

## Debugging Tips

1. **Increase logging verbosity**: Set `debug_level` to 4 in `config.json` for maximum logging detail.
2. **Check log files**: Review the log files in your specified logging directory for detailed error messages and execution flow.
3. **Use a debugger**: For Python-savvy users, use a debugger like pdb or an IDE's debugging tools to step through the code.
4. **Isolate the problem**: If possible, try to reproduce the issue with a single indexer or a smaller dataset.
5. **Check for updates**: Ensure you're using the latest version of the Copyright Protection Tool and all its dependencies.

Remember, if you encounter a persistent issue that you can't resolve, don't hesitate to open an issue on the project's GitHub page with a detailed description of the problem and steps to reproduce it.