from django.shortcuts import render
from .models import Film

def film_list(request):
    films = Film.objects.all()

    genre_filter = request.GET.get('genre', None)
    if genre_filter:
        films = films.filter(genre=genre_filter)

    rating_filter = request.GET.get('rating', None)
    if rating_filter:
        films = films.filter(rating__gte=rating_filter)

    return render(request, 'film_app/film_list.html', {'films': films})