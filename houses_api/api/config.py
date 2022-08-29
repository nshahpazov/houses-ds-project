"""Main configuration of our houses api server"""
import logging
from logging.handlers import TimedRotatingFileHandler
import pathlib
import os
import sys

PACKAGE_ROOT = pathlib.Path(__file__).resolve().parent.parent.parent

FORMATTER = logging.Formatter(
    "%(asctime)s — %(name)s — %(levelname)s —"
    "%(funcName)s:%(lineno)d — %(message)s")


# xTODO: READ about flask, docs, etc
# log directory configuration
LOG_DIR = PACKAGE_ROOT / 'logs'
LOG_DIR.mkdir(exist_ok=True)
LOG_FILE = LOG_DIR / 'ml_api.log'

# dataset paths
DATA_DIR = PACKAGE_ROOT / 'data'
TEST_DATASET_PATH = DATA_DIR / 'raw/test.csv'

# uploads directory configuration
UPLOAD_FOLDER = PACKAGE_ROOT / 'uploads'
UPLOAD_FOLDER.mkdir(exist_ok=True)
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])

# logging handlers
# xTODO: move to logging config file
def get_console_handler():
    """TODO"""
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(FORMATTER)
    return console_handler


def get_file_handler():
    """TODO"""
    file_handler = TimedRotatingFileHandler(LOG_FILE, when='midnight')
    file_handler.setFormatter(FORMATTER)
    file_handler.setLevel(logging.WARNING)
    return file_handler


def get_logger(*, logger_name):
    """Get logger with prepared handlers."""

    logger = logging.getLogger(logger_name)

    logger.setLevel(logging.INFO)

    logger.addHandler(get_console_handler())
    logger.addHandler(get_file_handler())
    logger.propagate = False

    return logger


# xTODO: main configuration, should read from environment or specific yaml files
# pylint: disable=too-few-public-methods
class Config:
    """
    Main config environment
    """
    DEBUG = False
    TESTING = False
    CSRF_ENABLED = True
    SECRET_KEY = 'this-really-needs-to-be-changed'
    SERVER_PORT = 5000
    UPLOAD_FOLDER = UPLOAD_FOLDER

# xTODO: main configuration, should read from environment or specific yaml files
# pylint: disable=too-few-public-methods
class ProductionConfig(Config):
    """
    Configuration for the production environment.
    Should use environment variables in the future, probably when
    docker is also introduced
    """
    DEBUG = False
    SERVER_ADDRESS: os.environ.get('SERVER_ADDRESS', '0.0.0.0')
    SERVER_PORT: os.environ.get('SERVER_PORT', '5000')

# xTODO: main configuration, should read from environment or specific yaml files
# pylint: disable=too-few-public-methods
class DevelopmentConfig(Config):
    """
    Configuration for the development environment.
    Should use environment variables in the future, probably when
    docker is also introduced
    """
    DEVELOPMENT = True
    DEBUG = True

# xTODO: main configuration, should read from environment or specific yaml files
# pylint: disable=too-few-public-methods
class TestingConfig(Config):
    """
    Configuration for the testing environment.
    Should use environment variables in the future, probably when
    docker is also introduced
    """
    TESTING = True
