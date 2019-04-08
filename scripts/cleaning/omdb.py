import numpy as np
import pandas as pd
import re

cols = ["imdbID", "Rated", "Genre", "Country", "Awards", "RottenTomatoes_Rating", "Metacritic_Rating"]
omdb = pd.read_csv("C://ws/netflox/output-tables/peti_final_omdb_list.csv", sep=';', usecols=cols, encoding = "ISO-8859-1", index_col=None, low_memory=False)

filter_list = pd.read_csv("C://ws/netflox/output-tables/imdb_sorted_reduced.csv", low_memory=False)
filtered = filter_list.merge(omdb, how="left", left_on="tconst", right_on="imdbID")
filtered.drop(["imdbID"], axis=1, inplace=True)
filtered.drop(filtered.columns[filtered.columns.str.contains("unnamed", case=False)], axis=1, inplace=True)

filtered.RottenTomatoes_Rating = filtered.RottenTomatoes_Rating.map[lambda r: int(r.replace("%", "")) if re.match(pattern, str(r)) else np.nan]
filtered.Metacritic_Rating = filtered.Metacritic_Rating.map[lambda r: int(r.replace("/100", "")) if re.match(pattern, str(r)) else np.nan]

def clean_awards(field):
    awards = []
    string = str(field)
    if "Oscar" in string:
        awards.append("Oscar")
    if "BAFTA" in string or "bafta" in string:
        awards.append("BAFTA")
    if "Golden Globe" in string:
        awards.append("GG")
    return ";".join(awards)

filtered.Awards = filtered.Awards.map(clean_awards)

categorical.fillna("", inplace = True)
categorical.Genre = categorical.Genre.str.replace(", ", ";")
categorical.Country = categorical.Country.str.replace(", ", ";")

filtered.to_csv("cleaned_omdb.csv", index=False)