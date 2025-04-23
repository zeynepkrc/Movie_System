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
    return render(request, 'home.html')

def recommend_films(request):
    if request.method == 'POST':
        genre = request.POST.get('genre')
        year = request.POST.get('year')
        duration = request.POST.get('duration')

        if not genre or not year or not duration:
            return render(request, 'home.html', {'error': 'All fields are required!'})

        try:
            year = int(year)
            duration = int(duration)
        except ValueError:
            return render(request, 'home.html', {'error': 'Year and duration must be integers!'})

        url = f'https://api.themoviedb.org/3/discover/movie?api_key={API_KEY}&with_genres={genre}&year={year}&with_runtime.lte={duration}&page=1'
        response = requests.get(url)
        data = response.json()
        movies = data.get('results', [])

        if not movies:
            return render(request, 'home.html', {'error': 'No films found based on your criteria.'})

        random_movies = random.sample(movies, min(3, len(movies)))

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

        return render(request, 'recommend.html', {
            'movies': random_movies,
            'genre_name': genre_name,
            'selected_year': year,
            'selected_duration': duration
        })

    return redirect('home')





