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
    logs = logs.select(
        logs['count_requests'],
        logs['sum_request_bytes']
    )

    logs = logs.groupby().agg(functions.sum('count_requests').alias('x'), functions.sum('sum_request_bytes').alias('y'),
                           functions.sum(logs['count_requests']**2).alias('x_sq'), functions.sum(logs['sum_request_bytes']**2).alias('y_sq'),
                           functions.sum(logs['count_requests'] * logs['sum_request_bytes']).alias('xy'), functions.count('count_requests').alias('n'))

    logs = logs.first()
    x = logs[0]
    y = logs[1]
    x_sq = logs[2]
    y_sq = logs[3]
    xy = logs[4]
    n = logs[5]

    # TODO: calculate r.

    r = (n*xy - x*y) / ((((n*x_sq) - x**2)**(0.5)) * (n*y_sq - y**2)**(0.5))

    print("r = %g\nr^2 = %g" % (r, r**2))

if __name__=='__main__':
    main()