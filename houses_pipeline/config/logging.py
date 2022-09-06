"""Configure the logging of the houses pipeline"""
import pathlib
import logging
from logging.handlers import TimedRotatingFileHandler
import sys

# pylint: disable=cyclic-import
import houses_pipeline
# Multiple calls to logging.getLogger('someLogger') return a
# reference to the same logger object.  This is true not only
# within the same module, but also across modules as long as
# it is in the same Python interpreter process.

PACKAGE_ROOT = pathlib.Path(houses_pipeline.__file__).resolve().parent
LOG_DIR = PACKAGE_ROOT / 'logs'
VERSION_PATH = PACKAGE_ROOT / 'VERSION'
LOG_FILE = LOG_DIR / 'pipeline.log'

FORMATTER = logging.Formatter(
    "%(asctime)s — %(name)s — %(levelname)s —"
     "%(funcName)s:%(lineno)d — %(message)s"
)


class LoggingHandler:
    """Factory class for creating logging handlers"""

    @staticmethod
    def __get_console_handler():
        """get the console handler"""
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setFormatter(fmt=FORMATTER)
        return console_handler

    @staticmethod
    def __get_file_handler():
        file_handler = TimedRotatingFileHandler(
            filename=LOG_FILE, when='midnight'
        )
        file_handler.setFormatter(fmt=FORMATTER)
        file_handler.setLevel(logging.INFO)
        return file_handler


    @staticmethod
    def create(logging_type='console'):
        """Create a logger"""
        if logging_type not in ['console', 'file']:
            raise ValueError("Not a proper type of logger")
        if logging_type == "console":
            return LoggingHandler.__get_console_handler()
        if logging_type == "file":
            return LoggingHandler.__get_file_handler()
        return None


    @staticmethod
    def get_logger(logger_name: str):
        """Get the main logger attaching console and file handling"""
        logger = logging.getLogger(logger_name)
        logger.setLevel(logging.DEBUG)

        # attach handlers
        logger.addHandler(LoggingHandler.__get_file_handler())
        logger.addHandler(LoggingHandler.__get_console_handler())

        logger.propagate = False
        return logger
