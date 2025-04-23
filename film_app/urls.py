from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('recommend/', views.recommend_films, name='recommend_films')
]