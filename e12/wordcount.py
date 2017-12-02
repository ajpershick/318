import sys
from pyspark.sql import SparkSession, functions, types
import string, re

spark = SparkSession.builder.appName('wordcount').getOrCreate()

assert sys.version_info >= (3, 4) # make sure we have Python 3.4+
assert spark.version >= '2.1' # make sure we have Spark 2.1+

# schema = types.StructType([ # commented-out fields won't be read
#     #types.StructField('archived', types.BooleanType(), False),
#     types.StructField('author', types.StringType(), False),
#     #types.StructField('author_flair_css_class', types.StringType(), False),
#     #types.StructField('author_flair_text', types.StringType(), False),
#     #types.StructField('body', types.StringType(), False),
#     #types.StructField('controversiality', types.LongType(), False),
#     #types.StructField('created_utc', types.StringType(), False),
#     #types.StructField('distinguished', types.StringType(), False),
#     #types.StructField('downs', types.LongType(), False),
#     #types.StructField('edited', types.StringType(), False),
#     #types.StructField('gilded', types.LongType(), False),
#     #types.StructField('id', types.StringType(), False),
#     #types.StructField('link_id', types.StringType(), False),
#     #types.StructField('name', types.StringType(), False),
#     #types.StructField('parent_id', types.StringType(), True),
#     #types.StructField('retrieved_on', types.LongType(), False),
#     types.StructField('score', types.LongType(), False),
#     #types.StructField('score_hidden', types.BooleanType(), False),
#     types.StructField('subreddit', types.StringType(), False),
#     #types.StructField('subreddit_id', types.StringType(), False),
#     #types.StructField('ups', types.LongType(), False),
# ])

def main():
    in_directory = sys.argv[1]
    out_directory = sys.argv[2]
    data = spark.read.text(in_directory)
    wordbreak = r'[%s\s]+' % (re.escape(string.punctuation),)  # regex that matches spaces and/or punctuation

    data = data.select(
        functions.lower(data['value']).alias('value')
    )

    data = data.select(
            functions.split(data['value'],wordbreak).alias('value')
    )

    data = data.select(
        functions.explode(data['value']).alias('word')
    )

    data = data[data['word'] != '']

    count = data.groupBy(data['word']).agg(functions.count(data['word']).alias('count'))
    count = count.sort(functions.desc('count'))
    count.show()

    count.write.csv(out_directory)

if __name__=='__main__':
    main()
