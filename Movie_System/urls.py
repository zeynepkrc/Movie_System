from django.contrib import admin
from django.urls import path
from film_app import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('recommend/', views.recommend_films, name='recommend_films')
]