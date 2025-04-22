# film_app/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.film_list, name='film_list'),
]
