import numpy as np
import pandas as pd

chunksize = 250000
chunks = []
for chunk in pd.read_csv('C://ws/netflox/data/sorted_imdb/imdb_sorted_reduced.csv', usecols=['tconst'], chunksize=chunksize, low_memory=False):
    chunks.append(chunk)
filter_list = list(pd.concat(chunks).tconst)

chunks = []
for chunk in pd.read_csv('C://ws/netflox/data/imdb-dataset/title_principals.tsv', sep="\t", chunksize=chunksize, low_memory=False):
    chunk = chunk.loc[chunk.tconst.isin(filter_list)]
    chunks.append(chunk[['tconst', 'nconst', 'category']])
filter_list = []
names = pd.concat(chunks)
names = names.loc[names.category.isin(['actor', 'actress', 'director', 'writer', 'self', 'composer', 'cinematographer'])]

name_counts = names.groupby("nconst").size().sort_values(ascending=False)
name_counts = name_counts.loc[name_counts > 1]
names = names.loc[names.nconst.isin(name_counts.index)]

def merge_names(row):
    tconst = row.tconst
    nconst = row.nconst
    if tconst in link_dict:
        link_dict[tconst] += ";" + nconst
    else:
        link_dict[tconst] = nconst
    return row

link_dict = {}
names.apply(merge_names, 1)
names = pd.DataFrame(list(link_dict.items()), columns=['tconst', 'names'])

names.to_csv("names.csv", index=False)
