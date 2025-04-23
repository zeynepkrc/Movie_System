import os
import sys
import requests
import django

# Django ayarlarını başlatmak için yolu ayarla
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Movie_System.settings')
django.setup()

from film_app.models import Film, Genre

# TMDb API anahtarını ayarlayın
API_KEY = 'f71beb95aabe859521b47f22127b2ec9'  # Buraya kendi API anahtarınızı girin

# TMDb genre ID'lerini eşleştirmek için harita
GENRE_MAP = {
    28: 'Action',
    12: 'Adventure',
    16: 'Animation',
    35: 'Comedy',
    80: 'Crime',
    99: 'Documentary',
    18: 'Drama',
    10751: 'Family',
    14: 'Fantasy',
    36: 'History',
    27: 'Horror',
    10402: 'Music',
    9648: 'Mystery',
    10749: 'Romance',
    878: 'Science Fiction',
    10770: 'TV Movie',
    53: 'Thriller',
    10752: 'War',
    37: 'Western'
}

def fetch_all_movies():
    page = 1
    while True:
        url = f'https://api.themoviedb.org/3/movie/popular?api_key={API_KEY}&language=en-US&page={page}'
        response = requests.get(url)
        data = response.json()

        if 'results' not in data or not data['results']:
            break

        for movie in data['results']:
            tmdb_id = movie['id']
            title = movie['title']
            release_year = int(movie['release_date'].split('-')[0]) if movie.get('release_date') else None
            poster_url = f"https://image.tmdb.org/t/p/w500{movie['poster_path']}" if movie.get('poster_path') else None

            film_obj, created = Film.objects.update_or_create(
                tmdb_id=tmdb_id,
                defaults={
                    'title': title,
                    'release_year': release_year,
                    'poster_url': poster_url,
                    'runtime': 0,  # Daha sonra detay endpointi ile alınabilir
                }
            )

            # Genre'leri ekle
            for genre_id in movie.get('genre_ids', []):
                genre_name = GENRE_MAP.get(genre_id)
                if genre_name:
                    genre_obj, _ = Genre.objects.get_or_create(name=genre_name)
                    film_obj.genres.add(genre_obj)

            print(f'Film "{title}" veritabanına kaydedildi.')

        page += 1

if __name__ == '__main__':
    fetch_all_movies()
