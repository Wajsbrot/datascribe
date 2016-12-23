# -*- coding: utf-8 -*-
"""
Created on Wed Jan 20 10:12:33 2016

@author: Nicolas Thiebaut
@email: nkthiebaut@gmail.com
"""

import os
import numpy as np
from openpyxl import load_workbook
import pandas as pd


def is_categorical(series, threshold=5):
    """ Return True if the input pandas.Series is categorical """
    return ((series.nunique() <= threshold) or
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


def df_to_excel_new_sheet(df, excelfile, sheetname='Dataframe', **kwargs):
    """ Write df in an excel file, in a new sheet if file already exists

    Parameters:
    -----------
    df: pandas.DataFrame
        input dataframe
    excelfile: str
        output excel file name
    sheename: str
        output excel sheet name (default: 'Dataframe')
    **kwargs: keyword arguments
        parameters passed to the pandas.DataFrame.to_excel function call"""
    if not os.path.exists(excelfile):
        df.to_excel(excelfile, sheetname=sheetname, **kwargs)
    else:
        book = load_workbook(excelfile)
        while sheetname in book.get_sheet_names():
            sheetname += '_new'
        writer = pd.ExcelWriter(excelfile, engine='openpyxl')
        writer.book = book
        writer.sheets = dict((ws.title, ws) for ws in book.worksheets)
        df.to_excel(writer, sheetname, **kwargs)
        writer.save()
