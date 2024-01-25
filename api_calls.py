from dotenv import load_dotenv
import os
import requests


load_dotenv()
TMDB_ACCESS_TOKEN = os.environ.get("TMDB_ACCESS_TOKEN")
OMDB_API_KEY = os.environ.get("OMDB_API_KEY")

tmdb_headers = {
    'Authorization': f'Bearer {TMDB_ACCESS_TOKEN}'
}
tmdb_get_movie_url = "https://api.themoviedb.org/3/search/movie"
tmdb_get_movie_details = "https://api.themoviedb.org/3/movie"
omdb_get_movie_url = "http://www.omdbapi.com"


def get_tmdb_movie_id(movie_name: str) -> int:
    response = requests.get(url=tmdb_get_movie_url, params={"query": movie_name}, headers=tmdb_headers)
    first_movie = response.json()['results'][0]
    
    return first_movie['id']


def get_movie_features(movie_name: str) -> str:
    movie_id = get_tmdb_movie_id(movie_name)

    tmdb_response = requests.get(url=f"{tmdb_get_movie_details}/{movie_id}",  headers=tmdb_headers)
    omdb_response = requests.get(url=omdb_get_movie_url, params = {"t": movie_name, "apikey": OMDB_API_KEY})

    tmdb_data = tmdb_response.json()
    omdb_data = omdb_response.json()

    features = ""

    for genre in tmdb_data['genres']:
        features += f"{genre['name']} "
    features += tmdb_data['overview']
    features += omdb_data['Actors'] + " "
    features += omdb_data['Director']
    modified_features = features.replace(",", "")
    
    return modified_features