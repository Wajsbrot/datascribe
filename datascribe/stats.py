# -*- coding: utf-8 -*-
"""
Created on Wed Jan 20 10:12:33 2016

@author: Nicolas Thiebaut
@email: nkthiebaut@gmail.com
"""

import logging
import numpy as np
import pandas as pd
from scipy.stats import shapiro, f, ttest_ind
from scipy.stats import contingency, chi2_contingency, fisher_exact
from .utils import is_categorical

# logging.config.fileConfig('logging.ini', disable_existing_loggers=False)


def test_normality(sample, alpha=0.05):
    """ Test if the given list has a normal distribution

    Parameters
    ----------
    sample: list
        input values
    alpha: float
        p-value threshold for normality hypothesis acceptance

    Returns
    -------
        bool: True if x came from a normally distributed population, else False
    """
    _, p_value = shapiro(sample)
    return p_value > alpha


def test_variances_equality(sample_a, sample_b, alpha=0.05):
    """ Return True if inputs variances are equal """
    var_a = np.var(sample_a)
    var_b = np.var(sample_b)
    if var_a == 0. or var_b == 0.:
        return False
    variance_ratio = var_a/var_b if var_a > var_b else var_b/var_a
    return variance_ratio < f.ppf(alpha/2, len(sample_a)-1, len(sample_b)-2)


def create_contingency_table(sample_a, sample_b):
    """ Output a contingency table from two samples lists w. same modalities"""
    counts_a = pd.Series(sample_a).value_counts().sort_index()
    counts_b = pd.Series(sample_b).value_counts().sort_index()
    if len(set(counts_a.index) & set(counts_b.index)) == 0:
        raise ValueError('The two columns contain different modalities')
    contingency_table = pd.concat([counts_a, counts_b], axis=1).fillna(0.)
    return contingency_table


def test_marginal_sums(contingency_table, threshold=5):
    """ Return True if the expected marginal sums are all above 5,
    in which case the chi square test of independency is generally
    considered valid"""
    expected_frequencies = contingency.expected_freq(contingency_table.values)
    return np.all(np.greater(expected_frequencies, threshold))


def compare_columns(sample_a, sample_b, categorical_threshold=5):
    """ Test difference of two columns using a series of tests to
    determine the most appropriate final test (e.g. chi2 if qualitative,
    t-test if numerical and homoscedastic, etc.) """
    if is_categorical(sample_a, categorical_threshold):
        if not is_categorical(sample_b, categorical_threshold):
            raise ValueError('Cannot determine if input columns are'
                             'categorical or numerical (number of modalities '
                             '{} and {})'.format(len(np.unique(sample_a)),
                                                 len(np.unique(sample_b))))
        contingency_table = create_contingency_table(sample_a, sample_b)
        logging.info("Contingency Table:\n"+str(contingency_table))
        test = "chi2"
        if test_marginal_sums(contingency_table):
            _, p_value, _, _ = chi2_contingency(contingency_table,
                                                correction=False)
        else:
            if contingency_table.shape[0] == 2:
                test = "fisher_exact"
                _, p_value = fisher_exact(contingency_table)
            else:
                _, p_value, _, _ = chi2_contingency(contingency_table)
    else:  # columns are numerical
        test = "student"
        # If variances are not equal: Welsch test instead of Student's
        use_welsch = test_variances_equality(sample_a, sample_b)
        _, p_value = ttest_ind(sample_a, sample_b, int(use_welsch),
                               nan_policy='omit')

    return test, p_value


def compare_common_columns(df_a, df_b, categorical_threshold=5):
    """ Test pairwise column difference with two input DataFrames """
    shared_cols = set(df_a.columns) & set(df_b.columns)
    tests_results = pd.DataFrame(columns=shared_cols,
                                 index=('test', 'p-value'))
    for col in shared_cols:
        logging.info("Columns compared: "+col)
        tests_results[col] = compare_columns(df_a[col], df_b[col],
                                             categorical_threshold)
    return tests_results


if __name__ == '__main__':
    size1 = 10
    size2 = 15
    num = list(range(size1-1))
    num.append(np.nan)
    df1 = pd.DataFrame({'bin': np.random.choice(['a', 'b'], size1),
                        'cat': np.random.choice(['a', 'b', 'c'], size1),
                        'num': num
                        })
    df2 = pd.DataFrame({'bin': np.random.choice(['a', 'b'], size2),
                        'cat': np.random.choice(['a', 'b', 'c'], size2),
                        'num': list(range(size2))
                        })
    print(compare_common_columns(df1, df2))
