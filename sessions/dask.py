# Copyright 2021 Cloudera, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# # dask Example

# Dask dataframes coordinate many Pandas dataframes along an index.
# Dask DF has a very similar API to Pandas.

# Dask DataFrame is used in situations where Pandas is commonly needed, usually when Pandas fails due to data size or computation speed.
# * If your dataset fits comfortably into RAM on your laptop, then you may be better off just using Pandas. There may be simpler ways to improve performance than through parallelism
# * If you need a proper database with all the common database capabilities, choose pySpark.

# The code in this file requires:
# * Python 3.6+
# * dask 0.25.0 or higher
# If this code fails to run in a Python 3 session, install the
# newest version of pandas by running `!pip install -U pandas`

# Out of all the flights, how many flights were late, and what
# was the average departure delay of late flights (in minutes)?

import dask.dataframe as dd

flights = dd.read_csv('data/flights.csv')
late_flights = flights[flights.arr_delay >= 30]

result = late_flights.groupby(late_flights.origin) \
          .agg({
            'arr_delay': ['mean'],
            'flight': ['size']
          }).compute() \
          .reset_index()

result.head()
