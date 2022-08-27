"""
The pipeline module containing extract, preprocess and train
"""
import pathlib
from .config.logging import LoggingHandler


PACKAGE_ROOT = pathlib.Path(__file__).resolve().parent
VERSION_PATH = PACKAGE_ROOT / 'VERSION'

# Configure logger for use in package
logger = LoggingHandler.get_logger(__name__)

# set the version as an importable module
with open(VERSION_PATH, 'r', encoding='utf-8') as version_file:
    __version__ = version_file.read().strip()
