from django.db import models

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







