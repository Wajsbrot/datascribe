# -*- coding:utf-8 -*-
"""
Created on the 09/01/17
@author: Nicolas Thiebaut
@email: nkthiebaut@gmail.com
"""

import argparse
from os import path
import pandas as pd
from datascribe.plots import make_plots_from_df

parser = argparse.ArgumentParser(
    description='Generates a description file for csv data files',
    formatter_class=argparse.ArgumentDefaultsHelpFormatter)

parser.add_argument('filename', metavar='filename', type=str,
                    help='csv data file name')
parser.add_argument('-s', '--sep', type=str, default=',',
                    help='field separator')
parser.add_argument('-d', '--dec', type=str, default='.',
                    help='decimal separator')
parser.add_argument('-o', '--outdir', type=str, default='figures',
                    help='output directory')
parser.add_argument('-n', '--name', type=str, default=None,
                    help='plots name (csv basename if None)')

args = parser.parse_args()
print("File: {}".format(args.filename))

df = pd.read_csv(args.filename, sep=args.sep, decimal=args.dec)
name = args.name
if not name:
    name = path.basename(args.filename)
make_plots_from_df(df, plot_name=name, plot_dir=args.outdir)
