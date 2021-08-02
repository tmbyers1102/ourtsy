from django.contrib import admin

from .models import ArtItem, Artist, Portfolio, Genres

admin.site.register(ArtItem)
admin.site.register(Artist)
admin.site.register(Portfolio)
admin.site.register(Genres)
