# Installation Guide for Copyright Protection Tool

This guide will walk you through the process of installing and setting up the Copyright Protection Tool on your system.

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [Installation Steps](#installation-steps)
3. [FlareSolverr Setup](#flaresolverr-setup)
4. [Configuration](#configuration)
5. [Verifying Installation](#verifying-installation)
6. [Troubleshooting](#troubleshooting)
7. [Next Steps](#next-steps)

## Prerequisites

Before you begin, ensure you have the following:

- Python 3.8 or higher installed on your system
- pip (Python package installer)
- Git (for cloning the repository)
- Docker (optional, required only if using FlareSolverr)

To check your Python version, run:
```
python --version
```

## Installation Steps

1. **Clone the Repository**

   Open a terminal and run:
   ```
   git clone https://github.com/G51DHU/copyright-protection-tool.git
   cd copyright-protection-tool
   ```

2. **Create a Virtual Environment**

   It's recommended to use a virtual environment to avoid conflicts with other Python projects:
   ```
   python -m venv venv
   ```

3. **Activate the Virtual Environment**

   - On Windows:
     ```
     venv\Scripts\activate
     ```
   - On macOS and Linux:
     ```
     source venv/bin/activate
     ```

4. **Install Dependencies**

   With the virtual environment activated, install the required packages:
   ```
   pip install -r requirements.txt
   ```

## FlareSolverr Setup

FlareSolverr is used to bypass anti-bot protections on some websites. If you need this functionality, follow these steps:

1. **Install Docker** (if not already installed)

   Follow the official Docker installation guide for your operating system: https://docs.docker.com/get-docker/

2. **Pull the FlareSolverr Docker Image**

   ```
   docker pull ghcr.io/flaresolverr/flaresolverr:latest
   ```

3. **Run FlareSolverr**

   ```
   docker run -d -p 8191:8191 -e LOG_LEVEL=info ghcr.io/flaresolverr/flaresolverr:latest
   ```

   This command runs FlareSolverr in detached mode, mapping port 8191.

## Configuration

1. **Create Configuration Files**

   Copy the example configuration files:
   ```
   cp config/config.example.json config/config.json
   cp config/supported_indexes.example.json config/supported_indexes.json
   ```

2. **Edit Configuration**

   Open `config/config.json` and `config/supported_indexes.json` in a text editor and adjust the settings according to your needs. Refer to the [Configuration Guide](CONFIGURATION.md) for detailed information on each setting.

3. **Set Up Output and Log Directories**

   Create directories for output and logs (if they don't exist):
   ```
   mkdir -p output logs
   ```

## Verifying Installation

To verify that the Copyright Protection Tool is installed correctly:

1. Ensure your virtual environment is activated.

2. Check that all required packages are installed:
   ```
   pip list
   ```
   Verify that you see all the packages listed in `requirements.txt`.

3. Run a basic check of the configuration:
   ```
   python -c "import json; print(json.load(open('config/config.json')))"
   ```
   This should display the contents of your configuration file. If you see an error, there might be an issue with your config.json file.

4. Verify that the main script can be run:
   ```
   python main.py
   ```
   
   If the installation is correct, you should see some initial log output, possibly including information about loading configurations and initializing indexers. The script may then start running indexers based on your configuration.

   Note: If it seems to hang, it might be attempting to run indexers. You can stop it with Ctrl+C.

5. Check the logs:
   After running the script, check the log file specified in your config.json (usually in the `logs` directory) for any error messages or warnings.

Remember, the actual behavior of the script will depend on your specific configuration. If it starts indexing immediately, you may want to review your `config/supported_indexes.json` file to ensure it only includes the indexers you want to run.

## Troubleshooting

If you encounter any issues during installation or initial setup:

1. **Dependency Issues**: 
   - Ensure you're using the correct Python version.
   - Try upgrading pip: `pip install --upgrade pip`
   - If a specific package is causing issues, try installing it separately.

2. **FlareSolverr Issues**:
   - Check if Docker is running correctly.
   - Ensure no other service is using port 8191.
   - Check FlareSolverr logs: `docker logs [container_id]`

3. **Configuration Errors**:
   - Validate your JSON files for correct syntax.
   - Ensure all required fields are present in the configuration files.

4. **Permission Issues**:
   - Ensure you have write permissions in the project directory for creating logs and output files.

5. **Script Hangs or Doesn't Respond**:
   - Check your `supported_indexes.json` file to ensure only the indexers you want to run are enabled.
   - Review the log files for any error messages or unexpected behavior.
   - Ensure you have a stable internet connection, especially if the tool is attempting to access external websites.

6. **Indexer-Specific Issues**:
   - If a particular indexer is causing problems, try disabling it in `supported_indexes.json` and run the script again.
   - Check if the target website for the indexer is accessible from your browser.

For more detailed troubleshooting, refer to the [Troubleshooting Guide](TROUBLESHOOTING.md).

If you continue to experience issues, please check the project's GitHub Issues page or reach out to the community for support.

## Next Steps

After successfully installing and verifying the Copyright Protection Tool:

1. Review the [Configuration Guide](CONFIGURATION.md) to fine-tune your settings.
2. Check the [README.md](README.md) for an overview of the tool's features and capabilities.
3. If you plan to contribute or add new indexers, read the [Contributing Guide](CONTRIBUTE.md) and [Adding Indexers Guide](ADDING_INDEXERS.md).

Happy indexing!