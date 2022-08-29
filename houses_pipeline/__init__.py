"""
The pipeline module containing extract, preprocess and train
"""
import pathlib
import joblib
from .config.logging import LoggingHandler
from .config.config import TRAINED_MODELS_DIR
from .preprocess.core import load_preprocess_pipeline


PACKAGE_ROOT = pathlib.Path(__file__).resolve().parent
VERSION_PATH = PACKAGE_ROOT / 'VERSION'

# Configure logger for use in package
logger = LoggingHandler.get_logger(__name__)

# set the version as an importable module
with open(VERSION_PATH, 'r', encoding='utf-8') as version_file:
    __version__ = version_file.read().strip()


def load_model(*, model_name):
    """Load a model from our model storage"""

    file_path = TRAINED_MODELS_DIR / model_name
    return joblib.load(filename=file_path)


def load_data(*, filename):
    """Load a dataset proxy method"""
    raise NotImplementedError("The loading of the data is not implemented yet")
    # file_path = TRAINED_MODELS_DIR / model_name
    # return joblib.load(filename=file_path)
