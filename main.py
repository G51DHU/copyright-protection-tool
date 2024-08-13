import logging
import os
import json
import importlib
import asyncio
from typing import Dict, Any

from validate import validate_config
from exceptions import ConfigurationError, IndexerError

def setup_logging(config: Dict[str, Any]) -> logging.Logger:
    log_path = os.path.abspath(config['logging_path'])
    os.makedirs(log_path, exist_ok=True)
    
    levels = [logging.DEBUG, logging.INFO, logging.WARNING, logging.ERROR, logging.CRITICAL]
    log_level = levels[config['debug_level']]
    
    logging.basicConfig(
        filename=os.path.join(log_path, 'main.log'),
        level=log_level,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    return logging.getLogger(__name__)

def get_config(path_for_config: str) -> Dict[str, Any]:
    if not os.path.exists(path_for_config):
        raise ConfigurationError(f"Config file does not exist: {path_for_config}")
    
    try:
        with open(path_for_config, "r") as f:
            return json.load(f)
    except json.JSONDecodeError:
        raise ConfigurationError(f"Invalid JSON in config file: {path_for_config}")
    except Exception as e:
        raise ConfigurationError(f"Error reading config file: {str(e)}")

def get_list_of_indexers(path_for_list_of_supported_indexes: str) -> Dict[str, Any]:
    if not os.path.exists(path_for_list_of_supported_indexes):
        raise ConfigurationError(f"Supported indexes file does not exist: {path_for_list_of_supported_indexes}")
    
    try:
        with open(path_for_list_of_supported_indexes, "r") as f:
            return json.load(f)
    except json.JSONDecodeError:
        raise ConfigurationError(f"Invalid JSON in supported indexes file: {path_for_list_of_supported_indexes}")
    except Exception as e:
        raise ConfigurationError(f"Error reading supported indexes file: {str(e)}")

async def main(path_for_config: str) -> None:
    try:
        config_dict = get_config(path_for_config)
        logger = setup_logging(config_dict)
        logger.info("----------")
        logger.info("Started")
        logger.info("----------")
        logger.info("Logging initialized")

        await validate_config(config_dict)

        logger.info("----------------")
        logger.info("Initialising")
        logger.info("----------------")
        
        logger.info("Setting path for where the supported indexes are stored")
        path_for_list_of_supported_indexes = config_dict["path_for_list_of_supported_indexes"]
        
        logger.info("Getting list of Indexes")
        list_of_indexers = get_list_of_indexers(path_for_list_of_supported_indexes)
        
        logger.info("----------------")
        logger.info("Successfully fetched: Config, Debugging level & Supported Indexes")
        logger.info("Initialisation complete")
        logger.info("----------------")
        
        for name, indexer_settings in list_of_indexers.items():
            logger.info(f"Found indexer of name: {name}")
            logger.info(f"Settings for this Indexer:\n{indexer_settings}")

            logger.info(f"Trying to import Indexer script from path: './indexers/{name}'")
            try:
                module = importlib.import_module(f".{name}", package="indexers")
            except ModuleNotFoundError:
                logger.error(f"Was not able to find the Indexer script from path: './indexers/{name}'")
                continue
                
            logger.info("Checking if indexer needs FlareSolverr")

            settings_to_use = {
                "base_url": indexer_settings["base_url"],
                "debug_level": config_dict["debug_level"],
                "output_dir": config_dict["output_dir"],
                "logging_path": config_dict["logging_path"]
            }
            to_check = ["fetch_concurrency_limit", "max_retries", "output_dir"]

            for key, value in indexer_settings["script_settings"].items():
                if (key == "fetch_concurrency_limit") and config_dict["fetch_concurrency_limit"]["use_as_global_max_concurrency_value"]:
                    settings_to_use[key] = config_dict["fetch_concurrency_limit"]["count"]
                    to_check.remove("fetch_concurrency_limit")
                elif (key == "max_retries") and config_dict["max_retries"]["use_as_global_max_retry_value"]:
                    settings_to_use[key] = config_dict["max_retries"]["count"]
                    to_check.remove("max_retries")
                elif indexer_settings.get("flaresolverr") is not None:
                    settings_to_use["flaresolverr_url"] = config_dict["flaresolverr"]["url"]
                    settings_to_use["flaresolverr_concurrency_limit"] = config_dict["flaresolverr"]["concurrency_limit"]
                else:
                    settings_to_use[key] = value
        
            for name_of_settings_left in to_check:
               settings_to_use[name_of_settings_left] = config_dict[name_of_settings_left]

            await module.handler(settings_to_use, logger)

    except ConfigurationError as e:
        logger.critical(f"Configuration error: {str(e)}")
    except IndexerError as e:
        logger.error(f"Indexer error: {str(e)}")
    except Exception as e:
        logger.critical(f"Unexpected error: {str(e)}", exc_info=True)

if __name__ == "__main__":
    PATH_FOR_CONFIG = "./config/config.json"
    asyncio.run(main(PATH_FOR_CONFIG))