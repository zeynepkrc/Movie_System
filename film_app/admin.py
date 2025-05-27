from django.contrib import admin
from .models import Film

admin.site.register(Film)
from .models import WatchedMovie
admin.site.register(WatchedMovie)
