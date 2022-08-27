"""
The pipeline module containing extract, preprocess and train
"""
import logging
import pathlib
from .config import logging_configuration


PACKAGE_ROOT = pathlib.Path(__file__).resolve().parent
VERSION_PATH = PACKAGE_ROOT / 'VERSION'

# Configure logger for use in package
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
logger.addHandler(logging_configuration.get_console_handler())
logger.propagate = False

# set the version as an importable module
with open(VERSION_PATH, 'r', encoding='utf-8') as version_file:
    __version__ = version_file.read().strip()
