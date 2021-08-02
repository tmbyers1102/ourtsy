from django.db import models
from django.db.models.signals import post_save
from leads.models import User


class ArtItem(models.Model):
    title = models.CharField(max_length=50)
    artist = models.ForeignKey("Artist", on_delete=models.CASCADE)

    def __str__(self):
        return self.title


class Genres(models.Model):
    name = models.CharField(max_length=100, blank=False)

    def __str__(self):
        return self.name


class Artist(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # institutuions = models.ManyToManyField(blank=True)
    # communities = models.ManyToManyField(blank=True)
    genres = models.ManyToManyField(Genres, blank=True)
    # mediums = models.ManyToManyField(blank=True)
    instagram = models.URLField(blank=True)
    twitter = models.URLField(blank=True)
    facebook = models.URLField(blank=True)
    bio = models.TextField(max_length=500, blank=True, null=True)


    def __str__(self):
        return self.user.username


# Whatever is added here has to be reconciled on the 'post_artist_created_signal' below
class Portfolio(models.Model):
    artist = models.OneToOneField(Artist, on_delete=models.CASCADE)

    def __str__(self):
        return self.artist.user.username



def post_artist_created_signal(sender, instance, created, **kwargs):
    if created:
        print(sender, instance)
        Portfolio.objects.create(artist=instance)


post_save.connect(post_artist_created_signal, sender=Artist)