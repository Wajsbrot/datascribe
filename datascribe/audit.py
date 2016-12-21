#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Wed Jan  6 18:49:02 2016

@author: Nicolas Thiebaut
@email: nkthiebaut@gmail.com
"""

from os.path import join, basename
import pandas as pd
from .utils import find_categorical


def audit_dataframe(df, n_top_values=10):
    """ Generate a description file for datas in a csv file

    Parameters
    ----------
    df: pandas.DataFrame
        input dataframe

    """
    def top_values(df, n_values=10, sep=', ', with_count=True):
        """ Retrieve most represented modalities for each column of a dataframe

        Parameters
        ----------
        df: pandas.DataFrame
            input dataframe
        n_values: int
            numbers of top modalities kept
        sep: str
            modalities separator in output column
        with_count: bool
            if True, write count of modalities in percent next to it

        Returns
        -------
        pandas.Series
            Series with the input DataFrame column names as indices, and the
            top modalities concatenated in a single line as values

        """
        ds = pd.Series([])
        for col_name in df:
            top = df[col_name].value_counts(normalize=True)\
                .iloc[:n_values]
            if with_count:
                top = [str(t)+' ('+str(round(100*top[t], 2))+' %)'
                       for t in top.index]
            else:
                top = top.index.astype(str)
            out = (sep).join(top)
            ds = ds.append(pd.Series([out], index=[col_name]))
        return ds

    raw_desc = df.describe(include='all').T

    null_percent = 100 * df.isnull().sum() / df.shape[0]
    null_percent = null_percent.to_frame(name='null_percent')

    nunique = df.apply(pd.Series.nunique).to_frame(name='n_unique')

    top = top_values(df, n_top_values).to_frame(name='top_'+str(n_top_values))

    cat_cols = find_categorical(df)
    col_type = pd.Series(raw_desc.index, index=raw_desc.index,
                         name='col_type').isin(cat_cols)
    col_type = col_type.apply(lambda x: 'cat' if x else 'num')

    desc = pd.concat([raw_desc, null_percent, col_type, nunique, top],
                     axis=1, copy=False)

    kept_columns = ['col_type', 'null_percent', 'n_unique', 'mean',
                    'min', 'max', 'top_10']

    return desc[kept_columns]


def make_audit_file(infile, desc_file=None, desc_dir='./out'):
    """ Generate a description file for datas in a csv file

    Parameters
    ----------
    infile: str
        csv file containing data
    desc_file: str
        csv file in which output is written
    desc_dir: str
        directory where description file is written

    """
    if desc_file is None:
        desc_file = join(desc_dir, basename(infile)[:-4] + '_desc.csv')

    df = pd.read_csv(infile, sep=';', decimal=',')
    audit_dataframe(df).to_csv(desc_file, sep=';', float_format='%.2f')
