from django.contrib import admin

from .models import ArtItem, Artist, Portfolio, Genres, Post, GenericStringTaggedItem

admin.site.register(ArtItem)
admin.site.register(Artist)
admin.site.register(Portfolio)
admin.site.register(Genres)
admin.site.register(Post)
admin.site.register(GenericStringTaggedItem)
