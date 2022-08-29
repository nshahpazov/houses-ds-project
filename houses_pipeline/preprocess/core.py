"""The main definition of our preprocessing steps"""
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import FunctionTransformer
from sklearn.impute import SimpleImputer
from ..transformers import Pandalizer
from .. import constants


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
