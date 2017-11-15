import sys
from pyspark.sql import SparkSession, functions, types

spark = SparkSession.builder.appName('wikipedia popular').getOrCreate()

assert sys.version_info >= (3, 4) # make sure we have Python 3.4+
assert spark.version >= '2.2' # make sure we have Spark 2.2+

schema = types.StructType([  # commented-out fields won't be read
    types.StructField('language', types.StringType(), False),
    types.StructField('name', types.StringType(), False),
    types.StructField('requests', types.LongType(), False),
    types.StructField('views', types.LongType(), False),
])

def main(in_directory, out_directory):
    data = spark.read.csv(in_directory, sep=' ', schema=schema).withColumn('filename', functions.input_file_name())
    



if __name__=='__main__':
    in_directory = sys.argv[1]
    out_directory = sys.argv[2]
    main(in_directory, out_directory)
    main(in_directory, out_directory)