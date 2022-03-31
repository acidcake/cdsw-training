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

## Command Line Parsing

# Start by loading the sys module
import sys

# Parse command-line arguments. This script expects
# one argument: the string `true` or `false.`
# By default we will not print schema.
if len(sys.argv) > 1 and sys.argv[1].lower() == 'false':
  will_print = False
else:
  will_print = True


import pyspark
from pyspark.sql import SparkSession

spark = SparkSession.builder \
  .appName('spark-job') \
  .getOrCreate()

flights = spark.read.csv('data/flights.csv', header=True, inferSchema=True)

if (willPrint):
    flights.printSchema()


spark.stop()
