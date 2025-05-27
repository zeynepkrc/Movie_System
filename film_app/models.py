from django.db import models
from django.contrib.auth.models import User

class Genre(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Film(models.Model):
    tmdb_id = models.IntegerField(null=True, blank=True)
    title = models.CharField(max_length=255)
    release_year = models.IntegerField()
    genres = models.ManyToManyField(Genre, related_name='films')
    runtime = models.IntegerField()  # Süre
    poster_url = models.URLField(blank=True, null=True)  # Poster URL

    def __str__(self):
        return self.title


def get_recommendations(user_genre, user_year, user_runtime):
    recommended_films = Film.objects.filter(
        genres__contains=[user_genre],
        release_date__year=user_year,
        runtime__gte=user_runtime - 15,
        runtime__lte=user_runtime + 15,
    )
    return recommended_films

class WatchedMovie(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    movie_id = models.IntegerField()  # TMDB ID
    title = models.CharField(max_length=255)
    poster_path = models.CharField(max_length=255)
    watched_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.title}"

class LikedMovie(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    movie_id = models.IntegerField()
    title = models.CharField(max_length=255)
    poster_path = models.CharField(max_length=255)
    liked_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.title}"

class WatchLaterMovie(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    movie_id = models.IntegerField()
    title = models.CharField(max_length=255)
    poster_path = models.CharField(max_length=255)
    added_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.title}"







