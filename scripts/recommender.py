import numpy as np
import pandas as pd
import sqlalchemy
import mysql.connector

engine = sqlalchemy.create_engine('mysql+mysqlconnector://username:password@localhost:3306/netflox', echo=False)

categories = ["titleType", "Rated", "Genre", "Country", "names", "artists", "production_companies", "Awards", "tags", "users"]

def get_movie_data(tconst, table):
    '''Get data from chosen table'''
    connection = engine.connect()
    statement = format("select * from %s where tconst='%s'" % (table, tconst))
    result = connection.execute(statement)
    return result.fetchone()

def get_attributes(movie):
    '''Merge columns of a movie'''
    movie_set = set()
    for cat in categories:
        movie_set.update(movie[cat].split(";"))
    movie_set.discard("")
    return movie_set

def merge_movies(tconsts):
    '''Merge a list of movies into one set'''
    merged_movie = set()
    for tconst in tconsts:
        merged_movie.update(get_attributes(get_movie_data(tconst, "categorical_data")))
    return merged_movie

def get_recommendations(similarities, num):
    '''Get a number of top recommendations from a dictionary of similarities'''
    return sorted(similarities, key=similarities.__getitem__, reverse=True)[0:num]

def get_titles(tconsts):
    '''Get the title & year for a movie'''
    titles = []
    for tconst in tconsts:
        title = get_movie_data(tconst, "titles")
        titles.append(title['primaryTitle'] + " (" + str(title['startYear']) + ")")
    return titles

movie_ids = ["tt0345273"]
taste = merge_movies(movie_ids)

connection = engine.connect()
cat_result = connection.execute("select * from categorical_data")

similarities = {}
for row in cat_result:
    similarities[row['tconst']] = len(taste.intersection(get_attributes(row)))

for movie in movie_ids:
    similarities.pop(movie)

titles = get_titles((get_recommendations(similarities, 15)))