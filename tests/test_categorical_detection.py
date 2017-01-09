# -*- coding:utf-8 -*-
"""
Created on the 19/12/16
@author: Nicolas Thiebaut
@email: nkthiebaut@gmail.com
"""

import numpy as np
import pandas as pd
from datascribe.utils import is_categorical

binary = pd.Series([1, 0, 1, 0, 1, 0])
categorical = pd.Series([0, 1, 2, 3, 4])
numerical = list(range(20))
numerical.append(np.nan)
numerical = pd.Series(numerical)


class TestCategoricalDetection(object):
    """ Test categorical columns detection """
    def test_single_categorical_detection(self):
        """ Check extreme cases of mean comparizon """
        for sample in [binary, categorical, numerical]:
            assert is_categorical(binary)
            assert is_categorical(categorical)
            assert not is_categorical(numerical)
