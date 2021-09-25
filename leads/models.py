from django.db import models
from django.db.models.signals import post_save
from django.db.models.deletion import CASCADE, SET_NULL
from django.contrib.auth.models import AbstractUser
from django.utils.text import slugify


class User(AbstractUser):
    is_organizer = models.BooleanField(default=True)
    is_agent = models.BooleanField(default=False)
    is_artist = models.BooleanField(default=False)
    is_reviewer = models.BooleanField(default=False)
    twitter_name = models.CharField(max_length=100, blank=True)
    twitter_url = models.URLField(blank=True)
    instagram_name = models.CharField(max_length=100, blank=True)
    instagram_url = models.URLField(blank=True)
    facebook_name = models.CharField(max_length=100, blank=True)
    facebook_url = models.URLField(blank=True)
    user_image = models.ImageField(default='default_user_image.jpg', upload_to='user_images')
    user_bg = models.ImageField(default='default_user_bg.jpg', upload_to='user_bgs')
    user_bio = models.TextField(max_length=500, blank=True, null=True)


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    slug = models.SlugField(max_length=50, primary_key=True)

    def __str__(self):
        return self.user.username


class Lead(models.Model):
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    age = models.IntegerField(default=0)
    organization = models.ForeignKey(UserProfile, on_delete=models.CASCADE, null=True)
    agent = models.ForeignKey("Agent", null=True, blank=True, on_delete=models.SET_NULL)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Agent(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    organization = models.ForeignKey(UserProfile, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.email


def post_user_created_signal(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance, slug=slugify(instance))


post_save.connect(post_user_created_signal, sender=User)