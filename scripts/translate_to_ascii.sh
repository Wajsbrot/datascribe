#!/usr/bin/env bash

# Convert file (first argument) to ascii 
# input: 1: infile name, 2: outfile name

iconv -f iso-8859-1 -t ascii//translit $1 > $2
