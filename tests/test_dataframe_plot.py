# -*- coding:utf-8 -*-
"""
Created on the 09/01/17
@author: Nicolas Thiebaut
@email: nkthiebaut@gmail.com
"""

from tempfile import tempdir
import pandas as pd
from datascribe.plots import make_plots_from_df

df = pd.read_csv('./data_sample')


class TestDataFramePlot(object):
    """ Test pandas.DataFrame descriptive plots """
    def test_plots_creation(self):
        """ Check DataFrame descriptive plots creation """
        make_plots_from_df(df, plot_dir=tempdir)


if __name__ == '__main__':
    import pytest
    pytest.main()

