from django.contrib import admin
from django.urls import path
from film_app import views
from django.urls import include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('recommend/', views.recommend_films, name='recommend_films'),
    path('accounts/', include('accounts.urls')),
    path('admin/', admin.site.urls),
    path('', include('film_app.urls')),
]