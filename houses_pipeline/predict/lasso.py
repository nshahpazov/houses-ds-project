"""Main pipeline endpoint for producing predictions with the lasso model"""
from typing import Union

import numpy as np
import pandas as pd

from .. import __version__
from ..validation import validate_inputs

from ..config import config
from ..config.logging import LoggingHandler

from .. import load_preprocess_pipeline
from .. import load_model
from .. import constants


_logger = LoggingHandler.get_logger(__name__)

# load the preprocessor
preprocessor = load_preprocess_pipeline()

# load the model
lasso_model_filnename = f"{config.LASSO_SAVE_FILENAME}_{__version__}.pkl"
lasso_model = load_model(model_name=lasso_model_filnename)


def predict(*, input_data: Union[pd.DataFrame, dict]) -> dict:
    """Make a prediction using a saved model pipeline.

    Args:
        input_data: Array of model prediction inputs.

    Returns:
        Predictions for each input row, as well as the model version.
    """

    # load the data and validate it
    input_df = pd.DataFrame(input_data)
    validated_df = validate_inputs(input_data=input_df)

    # preprocess the data
    to_impute = np.append(constants.CATEGORICAL_COLUMNS, constants.ORDINALS)
    processed_df = preprocessor.fit_transform(
        validated_df, impute_missing_categories__columns=to_impute
    )

    # produce predictions
    _logger.info("Making predictions with model version: %s", __version__)
    predictions = lasso_model.predict(processed_df).tolist()

    result = {
        'predictions': predictions,
        'version': __version__
    }

    return result
