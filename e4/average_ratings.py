import pandas as pd
import sys
import difflib
import numpy as np

def fixMatches (listElem):
    if len(listElem) > 0:
        return listElem[0]
    else:
        return np.nan

movie_list = sys.argv[1]
movie_ratings = sys.argv[2]
output = sys.argv[3]
movie_list_df = pd.read_table(movie_list, header=None)
movie_ratings_df = pd.read_table(movie_ratings)
movie_ratings_df['ratings'] = movie_ratings_df['title,rating'].str.extract(".*,\\s*(.*)", expand=False) # Finds rating after last comma
movie_ratings_df['title'] = movie_ratings_df['title,rating'].apply(lambda x: x.split(',')[0])
movie_ratings_df = movie_ratings_df.drop('title,rating', 1)
movie_ratings_df['title'] = movie_ratings_df['title'].apply(lambda x: difflib.get_close_matches(x, movie_list_df[0]))
movie_ratings_df['title'] = movie_ratings_df['title'].apply(lambda x: fixMatches(x))

movie_ratings_df = movie_ratings_df.dropna()
movie_ratings_df = movie_ratings_df.sort_values('title')
movie_ratings_df['ratings'] = movie_ratings_df['ratings'].astype(int)
movie_ratings_df = movie_ratings_df.groupby(['title']).mean()
movie_ratings_df.to_csv(output)
print(movie_ratings_df)
