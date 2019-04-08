import numpy as np
import pandas as pd

chunksize = 500000
chunks = []
for chunk in pd.read_csv("C://ws/ml-20m/genome-scores.csv", chunksize=chunksize, low_memory=False):
    chunks.append(chunk)
scores = pd.concat(chunks)

chunks = []
for chunk in pd.read_csv("C://ws/ml-20m/genome-tags.csv", chunksize=chunksize, low_memory=False):
    chunks.append(chunk)
tags = pd.concat(chunks)

linked_tags = scores.merge(tags, how="left", on="tagId")

chunks = []
for chunk in pd.read_csv("C://ws/ml-20m/links.csv", chunksize=chunksize, low_memory=False):
    chunks.append(chunk)
links = pd.concat(chunks)
links.imdbId = links.imdbId.map(lambda id: "tt" + (7-len(str(id)))*"0" + str(id))

linked_tags = linked_tags.merge(links, how="left", on="movieId")
linked_tags.drop(["movieId", "tagId", "tmdbId"], axis=1, inplace=True)
linked_tags[["imdbId", "tag", "relevance"]].to_csv("linked-genome-tags.csv")

chunks = []
for chunk in pd.read_csv("C://ws/ml-20m/ratings.csv", chunksize=chunksize, low_memory=False):
    chunks.append(chunk)
ratings = pd.concat(chunks)

linked_ratings = ratings.merge(links, how="left", on="movieId")
linked_ratings.drop(["timestamp", "tmdbId", "movieId"], axis=1, inplace=True)
linked_ratings[["imdbId", "userId", "rating"]].to_csv("movielens-linked-ratings.csv")