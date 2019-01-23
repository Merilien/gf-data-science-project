import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

chunksize = 500000

chunks = []
for chunk in pd.read_csv("C://ws/ml-20m/ratings.csv", chunksize=chunksize, low_memory=False):
    chunks.append(chunk)
ratings = pd.concat(chunks)

chunks = []
for chunk in pd.read_csv("C://ws/ml-20m/links.csv", chunksize=chunksize, low_memory=False):
    chunks.append(chunk)
links = pd.concat(chunks)
links.imdbId = links.imdbId.map(lambda id: "tt" + (7-len(str(id)))*"0" + str(id))

linked_ratings = ratings.merge(links, how="left", on="movieId")
ratings = ''
linked_ratings.drop(["timestamp", "tmdbId", "movieId"], axis=1, inplace=True)
linked_ratings[["imdbId", "userId", "rating"]].to_csv("movielens-linked-ratings.csv")
linked_ratings = ''

chunks = []
for chunk in pd.read_csv("C://ws/ml-20m/movies.csv", chunksize=chunksize, low_memory=False):
    chunks.append(chunk)
movies = pd.concat(chunks)

linked_genres = movies.merge(links, on="movieId")
linked_genres.drop(["tmdbId", "movieId", "title"], axis=1, inplace=True)

def search_genres(row):
    genres = row.genres.split("|")
    for genre in genres:
        if genre not in genre_list:
            genre_list.append(genre)
    return row
genre_list = []
linked_genres.apply(search_genres, axis="columns")
for genre in genre_list[:-1]:
    linked_genres[genre] = pd.Series(linked_genres.genres.str.contains(genre), index=linked_genres.index)
linked_genres.drop("genres", axis=1, inplace=True)
linked_genres.to.csv("movielens_genres.csv")
