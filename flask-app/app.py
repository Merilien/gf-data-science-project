import sys, os
from flask import Flask, render_template, redirect, request
from jinja2 import Environment, FileSystemLoader
import sqlalchemy
import mysql.connector

application = Flask(__name__)
env = Environment(loader=FileSystemLoader('templates/'))
sql_url = 'mysql+mysqlconnector://'+ os.environ["USERNAME"]+':' + os.environ["PASSWORD"] + '@localhost:3306/netflox'
engine = sqlalchemy.create_engine(sql_url, echo=False)

def load_titles():
    connection = engine.connect()
    result = connection.execute("select * from titles")
    d = {}
    for r in result:
        d[r['tconst']] = r['full_title']
    return d

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


@application.route('/', methods=['GET'])
def home():
    template = env.get_template('index.html')
    return template.render(movies=load_titles())

@application.route('/recommendations', methods=['POST'])
def recommendations():
    recs = recommend(request.selected)
    template = env.get_template('recommendations.html')
    return template.render(recommends=recs)

def recommend(movie_ids):
    taste = merge_movies(movie_ids)
    connection = engine.connect()
    cat_result = connection.execute("select * from categorical_data")
    similarities = {}
    for row in cat_result:
        similarities[row['tconst']] = len(taste.intersection(get_attributes(row)))
    for movie in movie_ids:
        similarities.pop(movie) 
    return get_recommendations(similarities, 15)


if __name__ == "__main__":
	application.run(host='0.0.0.0', port=8000)