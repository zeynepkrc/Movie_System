from django.shortcuts import render, redirect
import requests
import random
from scripts.fetch_tmdb import API_KEY

GENRE_DICT = {
    "28": "Action",
    "12": "Adventure",
    "16": "Animation",
    "35": "Comedy",
    "80": "Crime",
    "99": "Documentary",
    "18": "Drama",
    "10751": "Family",
    "14": "Fantasy",
    "36": "History",
    "27": "Horror",
    "10402": "Music",
    "9648": "Mystery",
    "10749": "Romance",
    "878": "Science Fiction",
    "10770": "TV Movie",
    "53": "Thriller",
    "10752": "War",
    "37": "Western"
}
def home(request):
    return render(request, 'film_app/home.html', {'genre_dict': GENRE_DICT})


def recommend_films(request):
    if request.method == 'POST':
        genre = request.POST.get('genre')
        year = request.POST.get('year')
        duration = request.POST.get('duration')

        if not genre:
            return render(request, 'film_app/home.html', {'error': 'Genre is required!'})

        try:
            year = int(year) if year else None
            duration = int(duration) if duration else None
        except ValueError:
            return render(request, 'film_app/home.html', {'error': 'Year and duration must be valid numbers!'})

        all_movies = []

        for page in range(1, 4):
            url = f'https://api.themoviedb.org/3/discover/movie?api_key={API_KEY}&with_genres={genre}&page={page}'
            if year:
                url += f"&year={year}"
            if duration:
                url += f"&with_runtime.lte={duration}"

            response = requests.get(url)
            if response.status_code != 200:
                continue

            data = response.json()
            movies = data.get('results', [])
            all_movies.extend(movies)

        if not all_movies:
            return render(request, 'film_app/home.html', {'error': 'No films found based on your criteria.'})

        random_movies = random.sample(all_movies, min(3, len(all_movies)))

        for movie in random_movies:
            movie_id = movie['id']
            detail_url = f'https://api.themoviedb.org/3/movie/{movie_id}?api_key={API_KEY}'
            detail_response = requests.get(detail_url)
            detail_data = detail_response.json()

            movie['runtime'] = detail_data.get('runtime', '-')
            movie['release_year'] = movie.get('release_date', '')[:4]
            rating = detail_data.get('vote_average')
            movie['rating'] = round(rating, 1) if rating is not None else '-'
            movie['overview'] = movie.get('overview', 'No description available.')

        genre_name = GENRE_DICT.get(genre, 'Unknown')

        return render(request, 'film_app/recommend.html', {
            'movies': random_movies,
            'genre_name': genre_name,
            'selected_year': year,
            'selected_duration': duration
        })

    return redirect('home')






