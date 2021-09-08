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

# Accessing a dataset hosted on AWS
# Authenticate to the AWS IAM user account by setting then
# environment variables AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY

# If you've run the requirements file, no reason to run the following line
# !pip install boto

# Create the Boto S3 connection object.
from boto.s3.connection import S3Connection
aws_connection = S3Connection()

# Download the dataset to the data directory
bucket = aws_connection.get_bucket('cdswdatatest')
key = bucket.get_key('highway_traffic.csv')
key.get_contents_to_filename('/home/cdsw/data/highway_traffic.csv')

# Now you can query this dataset using the tool of your choice.
# Since this is a very large data set, you should use
# Spark to filter the dataset before visualization.
# For more info, see the pyspark section of the course.

!hdfs dfs -mkdir data
!hdfs dfs -put data/highway_traffic.csv data/

import pyspark
from pyspark.sql import SparkSession

spark = SparkSession.builder \
  .appName('traffic_control') \
  .getOrCreate()
