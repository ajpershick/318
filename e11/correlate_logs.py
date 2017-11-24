import sys
from pyspark.sql import SparkSession, functions, types, Row
import re
spark = SparkSession.builder.appName('correlate logs').getOrCreate()

assert sys.version_info >= (3, 4) # make sure we have Python 3.4+
assert spark.version >= '2.1' # make sure we have Spark 2.1+

line_re = re.compile("^(\\S+) - - \\[\\S+ [+-]\\d+\\] \"[A-Z]+ \\S+ HTTP/\\d\\.\\d\" \\d+ (\\d+)$")


def line_to_row(line):
    """
    Take a logfile line and return a Row object with hostname and bytes transferred. Return None if regex doesn't match.
    """
    m = line_re.match(line)
    if m:
        return Row(host=m.groups()[0], num_bytes=m.groups()[1])
    else:
        return None

def not_none(row):
    """
    Is this None? Hint: .filter() with it.
    """
    return row is not None


def create_row_rdd(in_directory):
    log_lines = spark.sparkContext.textFile(in_directory)
    # TODO: return an RDD of Row() objects
    return log_lines.map(line_to_row).filter(not_none)

def main():
    in_directory = sys.argv[1]
    logs = spark.createDataFrame(create_row_rdd(in_directory))
    logs.cache()
    logs = logs.groupby('host').agg(functions.count('host').alias('count_requests'), functions.sum('num_bytes').alias('sum_request_bytes'))

    # TODO: calculate r.
    x = logs.groupby().sum().first()[0]
    y = logs.groupby().sum().first()[1]
    x_squared = logs['first()[0]
    y = logs.first()[1]
    n = 1
    r = ((n*x*y) - (x*y)) / ((n*x^2) - ())

    print("r = %g\nr^2 = %g" % (r, r**2))

if __name__=='__main__':
    main()