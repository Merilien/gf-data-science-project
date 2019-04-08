import numpy as np
import pandas as pd
import re

chunksize = 500000
chunks = []
for chunk in pd.read_csv('C://ws/netflox/data/imdb-dataset/title_basics.tsv', sep="\t", chunksize=chunksize, low_memory=False):
    chunks.append(chunk)
basics = pd.concat(chunks)

basics.drop(['originalTitle', 'genres', 'isAdult'], 1, inplace=True)
shifted=[4725290, 5474099, 5147525, 2973285, 2247604]
basics.drop(shifted, axis='index', inplace=True)

chunks = []
for chunk in pd.read_csv('C://ws/netflox/data/imdb-dataset/title_ratings.tsv', sep="\t", chunksize=chunksize, low_memory=False):
    chunks.append(chunk)
ratings = pd.concat(chunks)

basics = basics.merge(ratings, on='tconst')

to_delete = ['video', 'videoGame', 'tvEpisode']
basics = basics.loc[~basics.titleType.isin(to_delete)]

sortedlist = pd.read_csv('C://ws/netflox/data/sorted_imdb/sorted_imdb.csv', usecols=['tconst'], low_memory=False)
filtered = sortedlist.merge(basics, how='inner', on='tconst')

pattern = re.compile(r"^\d{4}$")
filtered.startYear = filtered.startYear.map(lambda year: int(year) if re.match(pattern, str(year)) else np.nan)
filtered.endYear = filtered.endYear.map(lambda year: int(year) if re.match(pattern, str(year)) else np.nan)
filtered.runtimeMinutes = filtered.runtimeMinutes.map(lambda time: int(time) if str(time).isnumeric() else np.nan)

filtered.fillna("", inplace = True)
filtered.to_csv("imdb_basics_cleaned.csv", index=False)