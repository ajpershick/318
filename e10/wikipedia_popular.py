import sys
import os
from pyspark.sql import SparkSession, functions, types

spark = SparkSession.builder.appName('wikipedia popular').getOrCreate()

assert sys.version_info >= (3, 4) # make sure we have Python 3.4+
assert spark.version >= '2.2' # make sure we have Spark 2.2+

schema = types.StructType([  # commented-out fields won't be read
    types.StructField('lang', types.StringType(), False),
    types.StructField('name', types.StringType(), False),
    types.StructField('views', types.LongType(), False),
    types.StructField('bytes', types.LongType(), False),
])

# https://stackoverflow.com/questions/678236/how-to-get-the-filename-without-the-extension-from-a-path-in-python
def convert_pathname(path):
    return os.path.splitext(path)[0][-15:-4]

def main(in_directory, out_directory):
    data = spark.read.csv(in_directory, sep=' ', schema=schema).withColumn('filename', functions.input_file_name())
    path_to_hour = functions.udf(convert_pathname, returnType = types.StringType())
    data = data.filter(data['lang'] == 'en')
    data = data.filter(data['name'] != 'Main_Page')
    data = data.filter(~data['name'].startswith('Special:'))

    data = data.select(
        data['lang'],
        data['name'],
        data['views'],
        data['bytes'],
        path_to_hour(data['filename']).alias("hour")
    )
    groupby_hour = data.groupBy("hour").agg(functions.max("views").alias('views'))

    groupby_hour = groupby_hour.cache()

    groupby_hour = groupby_hour.select(
        groupby_hour['hour'],
        groupby_hour['views']
    )

    data = data.join(groupby_hour, ['hour', 'views'])
    data = data.orderBy('hour')
    data = data.select(
        data['hour'],
        data['name'],
        data['views']
    )
    data.write.csv(out_directory + '-wiki', mode='overwrite')

if __name__=='__main__':
    in_directory = sys.argv[1]
    out_directory = sys.argv[2]
    main(in_directory, out_directory)