from models import retrieve_popular, movie_details_, search_movie, retrieve_similar, movie_trailer, retrieve_by_genre, movie_providers
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
    return render_template('movie_search.html', search_data=data, search=movie_name)

@app.route('/<movie_name>', methods=['GET', 'POST'])
def movie_details(movie_name):
    if request.method == 'POST':
        movie_name = request.form.get('movie_name')
        data = search_movie(movie_name)
        return render_template('movie_search.html', search_data=data, search=movie_name)
    elif request.method == 'GET':
        data = movie_details_(movie_name)
        similar = retrieve_similar(movie_name)
        trailer = movie_trailer(movie_name)
        providers = movie_providers(movie_name)
        return render_template('movie_details.html', data=data, similar=similar, trailer=trailer, providers=providers)

@app.route('/gêneros/<genre>', methods=['GET', 'POST'])
def by_genre(genre):
    if request.method == 'POST':
        movie_name = request.form.get('movie_name')
        data = search_movie(movie_name)
        return render_template('movie_search.html', search_data=data, search=movie_name)

    elif request.method == 'GET':
        genre_data = retrieve_by_genre(genre)
        genre_names = {'28': 'Ação', '12': 'Aventura', '16': 'Animação', '35': 'Comédia', '80': 'Crime', '99': 'Documentário', '18': 'Drama',
                   '10751': 'Família', '14': 'Fantasia', '27': 'Terror', '36': 'História', '10402': 'Música', '9648': 'Mistério', '10749': 'Romance',
                   '878': 'Ficção Científica', '10770': 'Cinema TV', '53': 'Thriller', '10752': 'Guerra', '37': 'Faroeste'}
        return render_template('filtered_genre.html', genre_data=genre_data, genre_name=genre_names[genre])

        
@app.errorhandler(500)
def not_found(e):
    return render_template('500.html')


app.run()