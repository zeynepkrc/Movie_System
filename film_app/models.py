from django.db import models

class Film(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    genre = models.CharField(max_length=100)
    release_year = models.IntegerField()
    rating = models.FloatField()

    def __str__(self):
        return self.title
