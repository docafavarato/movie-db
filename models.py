import requests
import tmdbsimple as tmdb
import concurrent.futures

def retrieve_popular():
    urls = [
        f'https://api.themoviedb.org/3/movie/popular?api_key=937aba2a3907c25e0509540bbe39f3a8&language=pt-br&page={i}' for i in range(50)
    ]

    session = requests.Session()
    def get_url(url):
        response = session.get(url)
        return response.json()

    movies = {}
    with concurrent.futures.ThreadPoolExecutor() as executor:
        results = [executor.submit(get_url, url) for url in urls]

        for future in concurrent.futures.as_completed(results):
            data = future.result()
            for i in range(19):
                try:
                    movies[data['results'][i]['title']] = [data['results'][i]['overview'], data['results'][i]['poster_path'], data['results'][i]['release_date'], data['results'][i]['id']]
                except:
                    continue

    return movies

def retrieve_similar(query):
    req = requests.get(f'https://api.themoviedb.org/3/movie/{query}/similar?api_key=937aba2a3907c25e0509540bbe39f3a8&language=pt-br&page=1')
    data = req.json()
    movies = {}
    for i in range(5):
        try:
            movies[data['results'][i]['title']] = [data['results'][i]['title'], data['results'][i]['poster_path'], data['results'][i]['id']]
        except:
            continue
    return movies


def movie_details_(query):
    tmdb.API_KEY = '937aba2a3907c25e0509540bbe39f3a8'
    request = tmdb.Movies(query)
    movie = request.info(language='pt-br')
    movie_info = {}
    
    movie_info['title'] = request.title
    movie_info['overview'] = request.overview
    movie_info['poster_path'] = request.poster_path
    movie_info['backdrop_path'] = request.backdrop_path
    movie_info['vote_average']= '{:.1f}'.format(request.vote_average)
    movie_info['int_vote_average']= int(request.vote_average)
    movie_info['vote_count'] = request.vote_count
    movie_info['release_date'] = request.release_date.replace('-', '/')

    return movie_info

def search_movie(query):
    tmdb.API_KEY = '937aba2a3907c25e0509540bbe39f3a8'
    search = tmdb.Search()
    movie = search.movie(query=query, language='pt-br')
    movies = {}
    count = 0
    for i in search.results:
        movies[movie['results'][count]['title']] = [movie['results'][count]['title'], movie['results'][count]['poster_path'], movie['results'][count]['id']]
        count += 1

    return movies
