==========
DataScribe
==========

-------------------
Description
-------------------
General csv files datasets exploration scripts and python utils. 


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

    from datascribe.utils import check_means_equality
    df = check_means_equality(df_a, df_b)

Scripts usage
.. code-block:: bash

    python audit.py file.csv

