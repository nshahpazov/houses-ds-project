"""Configure the logging of the houses pipeline"""
import logging
import sys


# Multiple calls to logging.getLogger('someLogger') return a
# reference to the same logger object.  This is true not only
# within the same module, but also across modules as long as
# it is in the same Python interpreter process.

LOG_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'


def get_console_handler():
    """get the console handler"""
    console_handler = logging.StreamHandler(sys.stdout)
    logging.basicConfig(level=logging.INFO, format=LOG_FORMAT)
    console_handler.setFormatter(LOG_FORMAT)
    return console_handler
