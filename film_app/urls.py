from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('recommend/', views.recommend_films, name='recommend_films'),
    path('mark-watched/', views.mark_watched, name='mark_watched'),
    path('mark-liked/', views.mark_liked, name='mark_liked'),
    path('mark-later/', views.mark_later, name='mark_later'),
    path('my-movies/', views.my_movies, name='my_movies'),
    path('watched/delete/<int:movie_id>/', views.delete_watched_movie, name='delete_watched_movie'),
    path('liked/delete/<int:movie_id>/', views.delete_liked_movie, name='delete_liked_movie'),
    path('later/delete/<int:movie_id>/', views.delete_watch_later_movie, name='delete_watch_later_movie'),

]
