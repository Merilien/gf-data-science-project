import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

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
scores = ''

chunks = []
for chunk in pd.read_csv("C://ws/ml-20m/links.csv", chunksize=chunksize, low_memory=False):
    chunks.append(chunk)
links = pd.concat(chunks)
links.imdbId = links.imdbId.map(lambda id: "tt" + (7-len(str(id)))*"0" + str(id))

linked_tags = linked_tags.merge(links, how="left", on="movieId")
linked_tags.drop(["movieId", "tagId", "tmdbId"], axis=1, inplace=True)

linked_tags[["imdbId", "tag", "relevance"]].to_csv("linked-genome-tags.csv")