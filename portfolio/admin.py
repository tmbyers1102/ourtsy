from django.contrib import admin

from .models import ArtCommunity, ArtItem, Artist, Portfolio, Post, GenericStringTaggedItem, ArtMedium, ArtGenre

admin.site.register(ArtItem)
admin.site.register(Artist)
admin.site.register(Portfolio)
admin.site.register(Post)
admin.site.register(GenericStringTaggedItem)
admin.site.register(ArtMedium)
admin.site.register(ArtCommunity)
admin.site.register(ArtGenre)

