# Getting Started with the Copyright Protection Tool

This guide will help you set up and run the Copyright Protection Tool for the first time.

## Prerequisites

- Python 3.8 or higher
- pip (Python package installer)
- Git (for cloning the repository)
- Docker (optional, required only if using FlareSolverr)

## Installation Steps

1. Clone the repository:
- git clone https://github.com/G51DHU/copyright-protection-tool.git
- cd copyright-protection-tool


2. Set up a virtual environment:
- python -m venv venv
- source venv/bin/activate  # On Windows use venv\Scripts\activate

3. Install dependencies:
- pip install -r requirements.txt

4. Configure the tool:
- Copy `config/config.example.json` to `config/config.json`
- Copy `config/supported_indexes.example.json` to `config/supported_indexes.json`
- Edit these files according to your needs (see [Configuration Guide](configuration.md) for details)

5. Run the tool:
- python main.py

## FlareSolverr Setup (Optional)

If you need to bypass anti-bot protections on some websites:

1. Install Docker if not already installed
2. Pull the FlareSolverr Docker image:

- docker pull ghcr.io/flaresolverr/flaresolverr:latest

3. Run FlareSolverr:
- docker run -d -p 8191:8191 -e LOG_LEVEL=info ghcr.io/flaresolverr/flaresolverr:latest

## Next Steps

- Read the [User Guide](user_guide.md) to learn how to use the tool effectively
- Check the [Configuration Guide](configuration.md) for detailed settings information
- If you encounter any issues, refer to the [Troubleshooting Guide](troubleshooting.md)

