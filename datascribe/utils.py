# -*- coding: utf-8 -*-
"""
Created on Wed Jan 20 10:12:33 2016

@author: Nicolas Thiebaut
@email: nkthiebaut@gmail.com
"""

import numpy as np
import pandas as pd


def is_categorical(series, threshold=5):
    """ Return True if the input pandas.Series is categorical """
    return ((series.nunique() <= threshold) or \
        (not np.issubdtype(series.dtype, np.number)))


def find_categorical(dataframe, threshold=5):
    """ Find categorical columns in dataframe

    Parameters
    ----------
    dataframe: pandas.DataFrame
        input dataframe
    threshold: int
        number of modalities below which a column is considered to be
        categorical, even if filled with ints of floats

    Returns
    -------
        list: categorical columns names
    """
    # count number of unique values in each column
    n_unique = dataframe.apply(pd.Series.nunique)
    categorical_cols = n_unique[n_unique <= threshold].index
    non_numerical_cols = \
        dataframe.select_dtypes(exclude=['int', 'float']).columns
    categorical_cols = set(categorical_cols).union(non_numerical_cols)
    return list(categorical_cols)
