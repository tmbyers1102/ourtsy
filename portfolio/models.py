from django.conf import settings
from django.db import models
from django.db.models.signals import post_save, pre_save
from leads.models import User, UserProfile
from django.utils.text import slugify

from taggit.managers import TaggableManager
from taggit.models import CommonGenericTaggedItemBase, TaggedItemBase


class GenericStringTaggedItem(CommonGenericTaggedItemBase, TaggedItemBase):
    object_id = models.CharField(max_length=50, verbose_name=('Object id'), db_index=True)


class ArtItem(models.Model):
    title = models.CharField(max_length=50)
    artist = models.ForeignKey("Artist", on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=8, decimal_places=2, default=50)
    slug = models.SlugField(max_length=50, primary_key=True, unique=True, blank=True)
    cover_image = models.ImageField(default='default_cover_image.jpg', upload_to='cover_images')
    tags = TaggableManager(through=GenericStringTaggedItem)

    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(ArtItem, self).save(*args, **kwargs)


class Post(models.Model):
    title = models.CharField(max_length=250)
    description = models.TextField()
    published = models.DateField(auto_now_add=True)
    slug = models.SlugField(unique=True, max_length=100)

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
    slug = models.SlugField(max_length=50, primary_key=True, unique=True, blank=True)
    artist_image = models.ImageField(default='default_artist_image.jpg', upload_to='artist_images')

    def __str__(self):
        return self.slug

    def save(self, *args, **kwargs):
        self.slug = slugify(self.user)
        super(Artist, self).save(*args, **kwargs)


# Whatever is added here has to be reconciled on the 'post_artist_created_signal' below
class Portfolio(models.Model):
    artist = models.OneToOneField(Artist, on_delete=models.CASCADE)
    slug = models.SlugField(max_length=50, primary_key=True)

    def __str__(self):
        return self.slug



def post_artist_created_signal(sender, instance, created, **kwargs):
    if created:
        print(sender, instance)
        Portfolio.objects.create(artist=instance, slug=slugify(instance))

post_save.connect(post_artist_created_signal, sender=Artist)


# def pre_artitem_created_signal(sender, instance, *args, **kwargs):
#     instance.slug = slugify(instance)


