import sys
from pyspark.sql import SparkSession, functions, types

spark = SparkSession.builder.appName('reddit relative scores').getOrCreate()

assert sys.version_info >= (3, 4) # make sure we have Python 3.4+
assert spark.version >= '2.1' # make sure we have Spark 2.1+

schema = types.StructType([ # commented-out fields won't be read
    #types.StructField('archived', types.BooleanType(), False),
    types.StructField('author', types.StringType(), False),
    #types.StructField('author_flair_css_class', types.StringType(), False),
    #types.StructField('author_flair_text', types.StringType(), False),
    #types.StructField('body', types.StringType(), False),
    #types.StructField('controversiality', types.LongType(), False),
    #types.StructField('created_utc', types.StringType(), False),
    #types.StructField('distinguished', types.StringType(), False),
    #types.StructField('downs', types.LongType(), False),
    #types.StructField('edited', types.StringType(), False),
    #types.StructField('gilded', types.LongType(), False),
    #types.StructField('id', types.StringType(), False),
    #types.StructField('link_id', types.StringType(), False),
    #types.StructField('name', types.StringType(), False),
    #types.StructField('parent_id', types.StringType(), True),
    #types.StructField('retrieved_on', types.LongType(), False),
    types.StructField('score', types.LongType(), False),
    #types.StructField('score_hidden', types.BooleanType(), False),
    types.StructField('subreddit', types.StringType(), False),
    #types.StructField('subreddit_id', types.StringType(), False),
    #types.StructField('ups', types.LongType(), False),
])

def main():
    in_directory = sys.argv[1]
    out_directory = sys.argv[2]

    comments = spark.read.json(in_directory, schema=schema)
    comments = comments.cache()

    data = comments.groupby('subreddit').agg(functions.avg('score'))
    data = data[data['avg(score)'] > 0]

    comments = comments.join(data, on='subreddit')
    comments = comments.withColumn('rel_score', comments['score']/comments['avg(score)'])

    max = comments.groupby('subreddit').agg(functions.max('rel_score'))

    comments = comments.join(max, on='subreddit')
    comments = comments[comments['rel_score'] == comments['max(rel_score)']]

    comments = comments.select(
        comments['subreddit'],
        comments['author'],
        comments['rel_score']
    )
    comments.write.json(out_directory, mode='overwrite')

if __name__=='__main__':
    main()
