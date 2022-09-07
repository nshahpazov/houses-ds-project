"""Main module to fetch the dataset by executing the fetch bash script"""
import os
from ..config.logging import LoggingHandler

logger = LoggingHandler.get_logger(logger_name=__name__)

def fetch_houses_dataset(path: str="data/raw"):
    """Fetch the dataset using the kaggle module"""
    # xTODO: change this to import and use kaggle instead of running bash scripts
    logger.info("fetching the data and unzipping it to %s", path)
    os.system("pwd")
    os.system("chmod +x ./houses_pipeline/fetch/fetch_dataset.sh")
    os.system(f"houses_pipeline/fetch/fetch_dataset.sh {path}")
