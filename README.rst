==========
DataScribe
==========

General csv, excel files, or pandas DataFrame exploration scripts and python utils. 
Includes descriptive statistics, versatile hypothesis testing and correlations analysis.

-------------------
Installation
-------------------
Clone the repository 

.. code-block:: bash 

    git clone https://github.com/wajsbrot/datascribe.git

Install the package from the datascribe folder

.. code-block:: bash

    pip install -e .
    
-------------------
Usage
-------------------
DataScribe contains both functions for use as a package and
scripts for creating csv plot or summaries.

-------------------
Example
-------------------
Package use in a python code

.. code-block:: python

    from datascribe.stats import compare_common_columns
    df = compare_common_columns(df_a, df_b)

Scripts usage

.. code-block:: bash

    audit.py my_file.csv

To use scripts one should add the scripts folder to the PATH 
environment variable, and to make the scripts executable with

.. code-block:: bash
 
    chmod +x /path_to_datascribe/scripts/*


