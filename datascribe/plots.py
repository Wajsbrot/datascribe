# -*- coding: utf-8 -*-
"""
Created on Thu Jan  7 18:37:55 2016

@author: Nicolas Thiebaut
@email: nkthiebaut@gmail.com
"""
from math import sqrt, ceil, floor
import os

import matplotlib
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter
import numpy as np
import seaborn as sns

from .utils import find_categorical

sns.set(color_codes=True)


def is_outlier(points, thresh=3.5):
    """
    Returns a boolean array with True if points are outliers and False
    otherwise.

    Parameters:
    -----------
    points : array
        An numobservations by numdimensions array of observations
    thresh : float
        The modified z-score to use as a threshold. Observations with
        a modified z-score (based on the median absolute deviation) greater
        than this value will be classified as outliers.

    Returns:
    --------
    array[bool]: A numobservations-length boolean array (mask).
    """
    if len(points.shape) == 1:
        points = points[:, None]
    median = np.median(points, axis=0)
    diff = np.sum((points - median)**2, axis=-1)
    diff = np.sqrt(diff)
    med_abs_deviation = np.median(diff)

    modified_z_score = 0.6745 * diff / med_abs_deviation

    return modified_z_score > thresh


def make_plots_from_df(df, plot_name='plot', plot_dir='figures',
                       max_modalities=10):
    """ Plot distribution for features in infile

    Parameters
    ----------
    df: pandas.DataFrame
        input dataframe
    max_modalities: int
        maximum number of different values for categorical features
    """
    def to_percent(y, position):
        """ Percent format for matplotlib """
        s = str(100 * y)

        # The percent symbol needs escaping in latex
        if matplotlib.rcParams['text.usetex'] is True:
            return s + r'$\%$'
        else:
            return s + '%'

    formatter = FuncFormatter(to_percent)
    plt.gca().yaxis.set_major_formatter(formatter)

    df.dropna(axis=1, how='all', inplace=True)  # remove empty columns
    for col in df.columns:
        if df[col].nunique() < 2:
            # remove mono-modality cols
            df.drop(col, axis=1, inplace=True)

    categorical_cols = find_categorical(df)

    # get rid of many-modalities columns
    categorical_cols = [c for c in df[categorical_cols]
                        if df[c].value_counts().shape[0] < max_modalities]

    numerical_cols = df.select_dtypes(include=['int', 'float']).columns
    numerical_cols = list(set(numerical_cols).difference(categorical_cols))

    # sns.pairplot(df[numerical_cols], size=5)

    # ----- Plot numerical features ----
    num_df = df[numerical_cols]
    num_df[(num_df >= num_df.quantile(0.1)) & (num_df <= num_df.quantile(0.9)) &
           (num_df != 0)].dropna(axis=0, how='any').hist(figsize=(20, 20), 
                                                         normed=True)

    if not os.path.exists(plot_dir):
        os.mkdir(plot_dir)
    plt.savefig(os.path.join(plot_dir, plot_name+'_numerical.png'))
    plt.clf()

    # ----- Plot categorical features ----
    n = len(categorical_cols)
    height = int(ceil(sqrt(n)))
    width = int(floor(sqrt(n)))
    fig, axes = plt.subplots(nrows=width, ncols=height,
                             figsize=(3*height, 3*width))

    for i in range(1, height*width-n+1):
        axes[-i, -1].axis('off')  # switch off unused subplots

    for i, c in enumerate(categorical_cols):
        x = i % width
        y = i % height
        df[c].value_counts(normalize=True, dropna=False).plot(kind='bar',
                                                              ax=axes[x, y])
        axes[x, y].set_title(c)
        axes[x, y].yaxis.set_major_formatter(formatter)
        axes[x, y].set_yticks([0, 0.2, 0.4, 0.6, 0.8, 1.])
    fig.tight_layout()
    plt.savefig(os.path.join(plot_dir, plot_name+'_categorical.png'))
