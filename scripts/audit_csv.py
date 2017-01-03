# -*- coding:utf-8 -*-
"""
Created on the 03/01/17
@author: Nicolas Thiebaut
@email: nkthiebaut@gmail.com
"""

import argparse
from os import path
import pandas as pd
from datascribe.audit import audit_dataframe

parser = argparse.ArgumentParser(
    description='Generates a description file for csv data files',
    formatter_class=argparse.ArgumentDefaultsHelpFormatter)

parser.add_argument('filenames', metavar='filenames', type=str, nargs='+',
                    help='csv data file names')
parser.add_argument('-s', '--sep', type=str, default=',',
                    help='field separator')
parser.add_argument('-d', '--dec', type=str, default='.',
                    help='decimal separator')

args = parser.parse_args()
print("Files: {}".format(args.filenames))

for f in args.filenames:
    df = pd.read_csv(f, sep=args.sep, decimal=args.dec)
    desc = audit_dataframe(df)
    desc.to_csv(path.basename(f)+'_desc.csv', sep=args['sep'], 
                decimal=args['dec'])
