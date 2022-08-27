"""
Test transformers
"""
from sklearn.impute import SimpleImputer
import pandas as pd
import numpy as np
from ..transformers import Pandalizer


def test_pandalizer_returns_dataframe():
    """Test whether the Pandalizer returns proper panda dataframe"""
    dataframe = pd.DataFrame({
        'x': [1, 2, 3, np.nan],
        'y': [np.nan, 12, 1.4,  5.6]
    })

    imputer = Pandalizer(SimpleImputer(strategy='mean'))
    result_dataframe = imputer.fit_transform(dataframe)
    assert isinstance(result_dataframe, pd.DataFrame)
