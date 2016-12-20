# -*- coding:utf-8 -*-
"""
Created on the 19/12/16
@author: Nicolas Thiebaut
@email: nthiebaut@quantmetry.com
"""

import numpy as np
import pandas as pd

from app.utils import compare_columns, compare_common_columns

binary = [1, 0, 1, 0, 1, 0]
categorical = [0, 1, 2, 3, 4]
numerical = list(range(20))
size1 = 20
size2 = 20
df1 = pd.DataFrame({'bin': np.random.choice(['a', 'b'], size1),
                    'cat': np.random.choice(['a', 'b', 'c'], size1),
                    'num': list(range(size1))})
df2 = pd.DataFrame({'bin': np.random.choice(['a', 'b'], size2),
                    'cat': np.random.choice(['a', 'b', 'c'], size2),
                    'num': list(range(size2))})


class TestStatisticalTests(object):
    """ Test automated statistical tests for pairs of DataFrames """
    def test_mean_comparizon(self):
        """ Check extreme cases of mean comparizon """
        for sample in [binary, categorical, numerical]:
            sample_series = pd.Series(sample)
            assert compare_columns(sample_series, sample_series)[1] == 1
            dummy_sample = pd.Series([0]*(len(sample)))
            assert compare_columns(sample_series, dummy_sample)[1] < 0.5

    def test_multiple_mean_comparizons(self):
        """ Check pairwise columns means equality tests """
        test = compare_common_columns(df1, df1)
        assert test.loc['p-value'].values.all() == 1
