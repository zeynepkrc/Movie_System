import requests
from django.conf import settings


def get_movie_data(title):
    api_key = settings.TMDB_API_KEY
    url = f"https://api.themoviedb.org/3/search/movie"
    params = {
        "api_key": api_key,
        "query": title,
        "language": "en-US"
    }
    response = requests.get(url, params=params)

    if response.status_code != 200:
        return None

    data = response.json()
    results = data.get("results", [])

    if not results:
        return None

    movie = results[0]  # En uygun eşleşme

    return {
        "title": movie.get("title"),
        "year": movie.get("release_date", "")[:4],
        "description": movie.get("overview"),
        "poster_url": f"https://image.tmdb.org/t/p/w500{movie.get('poster_path')}" if movie.get(
            "poster_path") else None,
        "rating": movie.get("vote_average")
    }