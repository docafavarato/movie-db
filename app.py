from models import retrieve_popular, movie_details_, search_movie, retrieve_similar, movie_trailer
from flask import Flask, render_template, request
import tmdbsimple as tmdb

app = Flask(__name__)

@app.route('/')
def index():
    data = retrieve_popular()
    return render_template('index.html', data=data)

@app.route('/', methods=['POST'])
def index_post():
    movie_name = request.form.get('movie_name')
    data = search_movie(movie_name)
    return render_template('movie_search.html', search_data=data)

@app.route('/<movie_name>')
def movie_details(movie_name):
    data = movie_details_(movie_name)
    similar = retrieve_similar(movie_name)
    trailer = movie_trailer(movie_name)
    return render_template('movie_details.html', data=data, similar=similar, trailer=trailer)

@app.errorhandler(500)
def not_found(e):
    return render_template('500.html')


app.run()