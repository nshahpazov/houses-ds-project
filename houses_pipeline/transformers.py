"""Data Transformers for helping with the preprocessing step"""
from sklearn.base import BaseEstimator, TransformerMixin
import pandas as pd
import numpy as np

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
    def __init__(self, threshold=0.05, keyword: str='Other') -> None:
        self.keyword = keyword
        self.threshold = threshold
        self.proportions = []


    def get_proportions(self, X):
        """
        Get the proportions of the keywords in the categorical columns
        """
        counts = [pd.Series(x).value_counts(normalize=True) for x in X.T]
        return counts


    def fit(self, X, y=None):
        """Fit the rare categorical transformer"""
        # pylint: disable=unused-argument
        is_df = isinstance(X, pd.DataFrame)
        self.proportions = self.get_proportions(X.values if is_df else X)
        return self


    def is_to_replace(self, i, col):
        """calculate keywords to replace by a given column"""
        props = self.proportions[i]
        rares = props[props < self.threshold].index.values
        new_ones = np.setdiff1d(col, props.index)
        is_rare = np.isin(col, rares)
        is_new_one = np.isin(col, new_ones)
        return is_rare | is_new_one


    def transform(self, X) -> pd.DataFrame:
        """Transform the rare categorical transformer"""
        is_df = isinstance(X, pd.DataFrame)
        Xt = X.values.copy() if is_df else X.values.copy()
        for i, col in enumerate(Xt.T):
            col[self.is_to_replace(i, col)] = self.keyword
        return Xt


class RedundantColumnsRemover(BaseEstimator, TransformerMixin):
    """
    Removes columns with a high proportion of repeating values
    """
    def __init__(self):
        self.columns_to_remove = None
        self.additional = None


    def _get_max_count(self, column):
        """Return the maximal value count for a categorical column"""
        category_props = column.value_counts(normalize=True)
        return category_props.max()


    def fit(self, X, y=None, threshold: float=0.9, additional: list[str]=None):
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
