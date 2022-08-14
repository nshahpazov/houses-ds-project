"""Data Transformers for helping with the preprocessing step"""
from sklearn.base import BaseEstimator, TransformerMixin
import pandas as pd
import numpy as np

from pipeline.preprocess import constants

class Pandalizer(BaseEstimator, TransformerMixin):
    """
    Executes a transformer on a subset of columns and returns a
    Pandas DataFrame as a result
    """
    def __init__(self, transformer):
        self.transformer = transformer
        self.columns = None


    def fit(self, df, y=None, columns=None, **fit_args):
        """Fit the Pandalizer taking additional fit_args to pass"""
        # get only a subset of columns on which to apply the transformer
        if columns is None:
            self.columns = df.columns
        else:
            self.columns = np.intersect1d(columns, df.columns)
        return self.transformer.fit(df[self.columns], y, **fit_args)


    def transform(self, data):
        """Transform the data"""
        df = data.copy()
        df.loc[:, self.columns] = self.transformer.transform(df[self.columns])
        return df


    def fit_transform(self, X, y=None, columns=None, **fit_args):
        """Fit_Transform the data"""
        # pylint: disable=unused-argument
        self.fit(X, y, columns, **fit_args)
        return self.transform(X)


class RareCategoriesReplacer(BaseEstimator, TransformerMixin):
    """
    Replaces Categorical Columns rare values with a keyword
    """
    def __init__(self, replace_keyword='Other', all_categories=None) -> None:
        self.replace_keyword = replace_keyword
        self.all_categories = all_categories
        self.columns = []
        self.rares = None


    def get_proportions(self, df, columns):
        """
        Get the proportions of the keywords in the categorical columns
        """
        value_counts = {k: df[k].value_counts(normalize=True) for k in columns}
        self.columns = []
        return value_counts


    def fit(self, X, y=None, columns:list[str]=None, threshold: float=0.05):
        """Fit the rare categorical"""
        # pylint: disable=unused-argument
        self.columns = columns or constants.CATEGORICAL_COLUMNS
        proportions = self.get_proportions(X, self.columns)
        items = proportions.items()

        # set the rare and all in order to transform
        self.all_categories = {k: v.index.values for k, v in items}
        self.rares = {k: list(l[l < threshold].index.values) for k, l in items}

        return self


    def transform(self, df: pd.DataFrame) -> pd.DataFrame:
        """Transform the rare categorical transformer"""
        result_df = df.copy()
        # must apply to each column
        for col in self.columns:
            # get keyswords not present in the all values
            uniques = result_df[col].unique()
            missing = np.setdiff1d(uniques, self.all_categories[col])

            # replace rare and not yet seen keywords
            result_df[col] = result_df[col].replace(
                to_replace=np.append(self.rares[col], missing),
                value=self.replace_keyword
            )
        return result_df


class MissingColumnsRemover(BaseEstimator, TransformerMixin):
    """
    Removes columns with a high proportion of missing values
    """
    def __init__(self):
        self.columns_to_drop = []


    def fit(self, X, y=None, threshold:float=0.8):
        """Learn which columns should be removed"""
        # pylint: disable=unused-argument
        null_props = X.isnull().mean(axis=0)
        self.columns_to_drop = null_props[null_props > threshold].index.values
        return self


    def transform(self, X):
        """Drop the columns which have missing value above the threshold"""
        return X.drop(self.columns_to_drop, axis=1)


class RedundantColumnsRemover(BaseEstimator, TransformerMixin):
    """
    Removes columns with a high proportion of repeating values
    """
    def __init__(self):
        self.columns_to_remove = None
        self.additional = None


    def _get_max_count(self, column: str):
        """Return the maximal value count for a categorical column"""
        category_props = column.value_counts(normalize=True)
        return category_props.max()


    def fit(self, X, y=None, threshold:float=0.9, additional: list[str]=None):
        """Learn the columns which are redundantly occupied"""
        # pylint: disable=unused-argument
        additional = [] if not additional else additional
        max_counts = X.apply(self._get_max_count, axis=0)
        above_threshold = max_counts[max_counts > threshold]
        self.columns_to_remove = above_threshold.index.values
        self.additional = additional
        return self


    def transform(self, X):
        """Drop the redundant columns plus additionally given ones"""
        columns_to_remove = np.append(
            self.columns_to_remove, self.additional
        )
        result = X.drop(columns_to_remove, axis=1)
        return result
