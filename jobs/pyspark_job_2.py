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


import pyspark
from pyspark.sql import SparkSession

spark = SparkSession.builder \
  .appName('spark-job') \
  .getOrCreate()

flights = spark.read.csv('data/flights.csv', header=True, inferSchema=True)

# ## Transforming Data

# Spark SQL provides a set of functions for manipulating
# Spark DataFrames. Each of these methods returns a
# new DataFrame.

# `select()` returns the specified columns:

flights.select('carrier').show()

# `distinct()` returns distinct rows:

flights.select('carrier').distinct().show()

# `filter()` (or its alias `where()`) returns rows that
# satisfy a Boolean expression.

# To disambiguate column names and literal strings,
# import and use the functions `col()` and `lit()`:

from pyspark.sql.functions import col, lit

flights.filter(col('dest') == lit('SFO')).show()

# `orderBy()` (or its alias `sort()`) returns rows
# arranged by the specified columns:

flights.orderBy('month', 'day').show()

flights.orderBy('month', 'day', ascending=False).show()

# `withColumn()` adds a new column or replaces an existing
# column using the specified expression:

flights \
  .withColumn('on_time', col('arr_delay') <= 0) \
  .show()

# To concatenate strings, import and use the function
# `concat()`:

from pyspark.sql.functions import concat

flights \
  .withColumn('flight_code', concat('carrier', 'flight')) \
  .show()

# `agg()` performs aggregations using the specified
# expressions.

# Import and use aggregation functions such as `count()`,
# `countDistinct()`, `sum()`, and `mean()`:

from pyspark.sql.functions import count, countDistinct

flights.agg(count('*')).show()

flights.agg(countDistinct('carrier')).show()

# Use the `alias()` method to assign a name to name the
# resulting column:

flights \
  .agg(countDistinct('carrier').alias('num_carriers')) \
  .show()

# `groupBy()` groups data by the specified columns, so
# aggregations can be computed by group:

from pyspark.sql.functions import mean

flights \
  .groupBy('origin') \
  .agg( \
       count('*').alias('num_departures'), \
       mean('dep_delay').alias('avg_dep_delay') \
  ) \
  .show()

# By chaining together multiple DataFrame methods, you
# can analyze data to answer questions. For example:

# How many flights to SFO departed from each airport,
# and what was the average departure delay (in minutes)?

flights \
  .filter(col('dest') == lit('SFO')) \
  .groupBy('origin') \
  .agg( \
       count('*').alias('num_departures'), \
       mean('dep_delay').alias('avg_dep_delay') \
  ) \
  .orderBy('avg_dep_delay') \
  .show()


# ## Using SQL Queries

# Instead of using Spark DataFrame methods, you can
# use a SQL query to achieve the same result.

# First you must create a temporary view with the
# DataFrame you want to query:

flights.createOrReplaceTempView('nyc_flights_2013')

# Then you can use SQL to query the DataFrame:

spark.sql("""
  SELECT origin,
    COUNT(*) AS num_departures,
    AVG(dep_delay) AS avg_dep_delay
  FROM nyc_flights_2013
  WHERE dest = 'SFO'
  GROUP BY origin
  ORDER BY avg_dep_delay""").show()


# ## Cleanup

# Stop the Spark application:

spark.stop()
