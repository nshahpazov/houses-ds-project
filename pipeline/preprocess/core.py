"""The core preprocessing steps to be imported and executed"""
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import OrdinalEncoder

from pipeline.preprocess import constants
from pipeline.preprocess.transformers import (MissingColumnsRemover,
    RedundantColumnsRemover, Pandalizer, RareCategoriesReplacer)

categories = [constants.ORDINALS_ORDERING] * len(constants.ORDINALS)
simple_imputer = SimpleImputer(strategy='constant', fill_value='Missing')

preprocessing_steps = [
    ('remove_nan_columns', MissingColumnsRemover()),
    ('remove_redundant_columns', RedundantColumnsRemover()),
    ('impute_missing_categories', Pandalizer(simple_imputer)),
    ('ordinals_encoding', Pandalizer(OrdinalEncoder(categories=categories))),
    ('replace_rare_categories', RareCategoriesReplacer())
]
