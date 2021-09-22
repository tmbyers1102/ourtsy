from django.contrib import admin

from .models import ArtCommunity, ArtItem, ArtStatus, Artist, Portfolio, Post, GenericStringTaggedItem, ArtMedium, ArtGenre, ApprovalStatus
from .models import (
    ArtCommunity,
    ArtItem,
    ArtStatus,
    Artist,
    Portfolio,
    Post,
    GenericStringTaggedItem,
    ArtMedium,
    ArtGenre,
    ApprovalStatus,
    ArtImage,
    PostStatus,
)


class PostsInline(admin.StackedInline):
    model = Post
 

class ArtImagesInline(admin.StackedInline):
    model = ArtImage


class ArtItemAdmin(admin.ModelAdmin):
    list_display = ['title', 'artist', 'price', 'slug']
    list_display_links = ['title']
    list_filter = ['artist', 'price']
    list_editable = ['price']
    inlines = [ArtImagesInline]
    fieldsets = (
        (None, {
            'fields': (('title', 'artist', 'price'), ('slug', 'art_status', 'cover_image'))
        }),
        ('ID Options', {
            'classes': ('collapse',),
            'fields': ('tags', 'art_story', 'art_mediums', 'art_genres', 'art_communities'),
        }),
        ('Approval Options', {
            'classes': ('collapse',),
            'fields': (('approval_status', 'date_submitted', 'publish_after_approved', 'urgent_review'), 'reviewed_by', 'review_note'),
        }),
    )


class ArtistAdmin(admin.ModelAdmin):
    inlines = [PostsInline]
    fieldsets = (
        (None, {
            'fields': ('user', 'slug')
        }),
        ('Social Options', {
            'classes': ('collapse',),
            'fields': ('instagram', 'twitter', 'facebook'),
        }),
        ('Bio Options', {
            'classes': ('collapse',),
            'fields': ('bio', 'art_mediums', 'art_genres', 'art_communities'),
        }),
        ('Image Options', {
            'classes': ('collapse',),
            'fields': ('artist_image', 'artist_headshot', 'studio_image'),
        })
    )


admin.site.register(ArtItem, ArtItemAdmin)
admin.site.register(Artist, ArtistAdmin)
admin.site.register(Portfolio)
admin.site.register(Post)
admin.site.register(GenericStringTaggedItem)
admin.site.register(ArtMedium)
admin.site.register(ArtCommunity)
admin.site.register(ArtGenre)
admin.site.register(ArtStatus)
admin.site.register(ApprovalStatus)
admin.site.register(ArtImage)
admin.site.register(PostStatus)

