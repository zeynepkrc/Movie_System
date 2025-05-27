from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse, HttpResponseBadRequest
from django.contrib.auth.decorators import login_required
import requests
import random
from .models import WatchedMovie, LikedMovie, WatchLaterMovie
from scripts.fetch_tmdb import API_KEY

GENRE_DICT = {
    "28": "Action", "12": "Adventure", "16": "Animation", "35": "Comedy",
    "80": "Crime", "99": "Documentary", "18": "Drama", "10751": "Family",
    "14": "Fantasy", "36": "History", "27": "Horror", "10402": "Music",
    "9648": "Mystery", "10749": "Romance", "878": "Science Fiction",
    "10770": "TV Movie", "53": "Thriller", "10752": "War", "37": "Western"
}

def home(request):
    return render(request, 'filmapp/home.html', {'genre_dict': GENRE_DICT})

def recommend_films(request):
    if request.method == 'POST':
        genre = request.POST.get('genre')
        year = request.POST.get('year')
        duration = request.POST.get('duration')

        if not genre:
            return render(request, 'filmapp/home.html', {
                'genre_dict': GENRE_DICT,
                'error': 'Genre is required!'
            })

        try:
            year = int(year) if year else None
            duration = int(duration) if duration else None
        except ValueError:
            return render(request, 'filmapp/home.html', {
                'genre_dict': GENRE_DICT,
                'error': 'Year and duration must be valid numbers!'
            })

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
            all_movies.extend(data.get('results', []))

        if not all_movies:
            return render(request, 'filmapp/home.html', {
                'genre_dict': GENRE_DICT,
                'error': 'No films found based on your criteria.'
            })

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
        return render(request, 'filmapp/recommend.html', {
            'movies': random_movies,
            'genre_name': genre_name,
            'selected_year': year,
            'selected_duration': duration
        })

    return redirect('home')

@login_required
def my_movies(request):
    return render(request, 'filmapp/my_movies.html', {
        'watched': WatchedMovie.objects.filter(user=request.user),
        'liked': LikedMovie.objects.filter(user=request.user),
        'later': WatchLaterMovie.objects.filter(user=request.user),
    })

@login_required
def mark_watched(request):
    if request.method == 'POST':
        movie_id = request.POST['movie_id']
        if not WatchedMovie.objects.filter(user=request.user, movie_id=movie_id).exists():
            WatchedMovie.objects.create(
                user=request.user,
                movie_id=movie_id,
                title=request.POST['title'],
                poster_path=request.POST['poster_path']
            )
            return JsonResponse({'status': 'ok', 'created': True})
        return JsonResponse({'status': 'exists', 'created': False})

@login_required
def mark_liked(request):
    if request.method == 'POST':
        movie_id = request.POST['movie_id']
        if not LikedMovie.objects.filter(user=request.user, movie_id=movie_id).exists():
            LikedMovie.objects.create(
                user=request.user,
                movie_id=movie_id,
                title=request.POST['title'],
                poster_path=request.POST['poster_path']
            )
            return JsonResponse({'status': 'ok', 'created': True})
        return JsonResponse({'status': 'exists', 'created': False})

@login_required
def mark_later(request):
    if request.method == 'POST':
        movie_id = request.POST['movie_id']
        if not WatchLaterMovie.objects.filter(user=request.user, movie_id=movie_id).exists():
            WatchLaterMovie.objects.create(
                user=request.user,
                movie_id=movie_id,
                title=request.POST['title'],
                poster_path=request.POST['poster_path']
            )
            return JsonResponse({'status': 'ok', 'created': True})
        return JsonResponse({'status': 'exists', 'created': False})

@login_required
def delete_watched_movie(request, movie_id):
    if request.method == "POST":
        get_object_or_404(WatchedMovie, id=movie_id, user=request.user).delete()
        return JsonResponse({'status': 'ok'})
    return JsonResponse({'status': 'invalid'}, status=400)

@login_required
def delete_liked_movie(request, movie_id):
    if request.method == "POST":
        get_object_or_404(LikedMovie, id=movie_id, user=request.user).delete()
        return JsonResponse({'status': 'ok'})
    return HttpResponseBadRequest("Invalid request")

@login_required
def delete_watch_later_movie(request, movie_id):
    if request.method == "POST":
        get_object_or_404(WatchLaterMovie, id=movie_id, user=request.user).delete()
        return JsonResponse({'status': 'ok'})
    return HttpResponseBadRequest("Invalid request")

