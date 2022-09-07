"""The main definition of our preprocessing steps"""
import pandas as pd
import numpy as np
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import FunctionTransformer
from sklearn.impute import SimpleImputer
from ..transformers import Pandalizer
from .. import constants


def preprocess(
    input_filepath: str=constants.DEFAULT_PREPROCESS_INPUT_PATH,
    output_filepath: str=constants.DEFAULT_PREPROCESS_OUTPUT_PATH,
    verbose: bool=True
) -> pd.DataFrame:
    """Entire preprocessing step as a single python function"""
    input_df = pd.read_csv(input_filepath)
    pipeline = load_preprocess_pipeline(verbose=verbose)

    # transform the data
    to_impute = np.append(constants.CATEGORICAL_COLUMNS, constants.ORDINALS)
    output_houses_dataframe = pipeline.fit_transform(
        input_df,
        impute_missing_categories__columns=to_impute
    )
    save_processed_df(output_houses_dataframe, output_filepath)
    return output_houses_dataframe


def load_preprocess_pipeline(verbose=False):
    """Load the preprocessing pipeline"""
    preprocess_pipeline = Pipeline(
        steps=[
            ('drop_useless_columns', FunctionTransformer(
                lambda df: df.drop(constants.DROP_COLUMNS, axis=1))
            ),
            ('impute_missing_categories', Pandalizer(
                SimpleImputer(strategy='constant', fill_value='Missing')
            ))
            # Usually this pipeline might also have:
            # removing duplicate rows
            # formatting dates
            # transforming types and scales to be the same, unification, etc
            # removing erroneous data

            # I would consider it doesn't have anything learnable from
            # the dataset, or experimentable.
        ],
        verbose=verbose
    )
    return preprocess_pipeline


def save_processed_df(df: pd.DataFrame, output_filepath: str) -> pd.DataFrame:
    """Save the dataframe wrapper"""
    # save the output to the specified path
    df.to_csv(output_filepath, index=False)
    return df
