from django.conf import settings
from django.db import models
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from leads.models import User, UserProfile
from django.utils.text import slugify
from django.utils import timezone
from taggit.managers import TaggableManager
from taggit.models import CommonGenericTaggedItemBase, TaggedItemBase
from django.utils.crypto import get_random_string
import random
import os


class HeroImage(models.Model):
    image = models.ImageField(upload_to='hero_images')
    file_name_text = models.CharField(max_length=100)
    unsplash_credit = models.TextField(max_length=500, blank=True, null=True)

    def __str__(self):
        return self.file_name_text

class GenericStringTaggedItem(CommonGenericTaggedItemBase, TaggedItemBase):
    object_id = models.CharField(max_length=50, verbose_name=('Object id'), db_index=True)



class ArtStatus(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name


class ApprovalStatus(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name


class ArtItem(models.Model):
    title = models.CharField(max_length=50)
    artist = models.ForeignKey("Artist", related_name="art_items", on_delete=models.CASCADE)
    #  old price field
    # price = models.DecimalField(max_digits=8, decimal_places=2, default=50)
    price = models.PositiveIntegerField(default=99)
    slug = models.SlugField(max_length=50, primary_key=True, unique=True, blank=True)
    cover_image = models.ImageField(default='default_cover_image.jpg', upload_to='cover_images')
    tags = TaggableManager(through=GenericStringTaggedItem)
    art_story = models.TextField(max_length=500, blank=True, null=True)
    art_mediums = models.ManyToManyField("ArtMedium", blank=True)
    art_communities = models.ManyToManyField("ArtCommunity", blank=True)
    art_genres = models.ManyToManyField("ArtGenre", blank=True)
    art_status = models.ForeignKey(ArtStatus, null=True, default=1, on_delete=models.SET_DEFAULT)
    approval_status = models.ForeignKey(ApprovalStatus, null=True, default=1, on_delete=models.SET_DEFAULT)
    date_submitted = models.DateTimeField(default=timezone.now)
    publish_after_approved = models.BooleanField(default=False)
    reviewed_by = models.ForeignKey(User, on_delete=models.DO_NOTHING, blank=True, null=True)
    review_note = models.TextField(max_length=1000, blank=True, null=True)
    urgent_review = models.BooleanField(default=False)
    # review_date

    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        self.slug = str(slugify(self.artist) + "_" + slugify(self.title))
        super(ArtItem, self).save(*args, **kwargs)


# this function reformats the images uploaded to take on the 
def rename_image_file(instance, filename):
    print('renaming the image file')
    # set path
    path = "art_images/"
    # get filename and strip off the .jpg part
    extension = str(instance.art_item)+str("_")
    # make a random int and make it a string
    randInt = get_random_string(8,'0123456789')
    print(str('new random int: ') + randInt )
    # i suppose i have to add jpg to end of this to make it a useable jpg
    jpg_str = str(".jpg")
    # reformat filename 
    filename_reformat = extension + randInt + jpg_str
    # join the new filename with the path and send to model instance!
    print(str(os.path.join(path, filename_reformat)))
    return os.path.join(path, filename_reformat)
    

class ArtImage(models.Model):
    art_item = models.ForeignKey(ArtItem, related_name="has_images", on_delete=models.CASCADE)
    image = models.ImageField(blank=True, upload_to=rename_image_file)

    def __str__(self):
        return str(self.image)


class PostStatus(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name


class Post(models.Model):
    title = models.CharField(max_length=250)
    author = models.ForeignKey(User, related_name="post_author", on_delete=models.CASCADE)
    mentioned_artists = models.ManyToManyField("Artist", blank=True)
    focus_artist = models.ForeignKey("Artist", related_name="has_artist", on_delete=models.CASCADE)
    description = models.TextField(max_length=200)
    text = models.TextField()
    published = models.DateField(auto_now_add=True)
    slug = models.SlugField(max_length=100, primary_key=True, unique=True, blank=True, editable = False)
    post_image = models.ImageField(default='default_post_image.jpg', upload_to='post_images')
    post_status = models.ForeignKey(PostStatus, null=True, default=1, on_delete=models.SET_DEFAULT)
    approval_status = models.ForeignKey(ApprovalStatus, null=True, default=1, on_delete=models.SET_DEFAULT)
    publish_after_approved = models.BooleanField(default=False)
    reviewed_by = models.ForeignKey(User, related_name="post_reviewer", on_delete=models.DO_NOTHING, blank=True, null=True)
    review_note = models.TextField(max_length=1000, blank=True, null=True)
    urgent_review = models.BooleanField(default=False)
    showcase = models.BooleanField(default=False)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.slug = self.slug or slugify(self.title)
        super(Post, self).save(*args, **kwargs)


class ArtMedium(models.Model):
    name = models.CharField(max_length=100, blank=False)
    description = models.TextField(max_length=500, blank=True, null=True)
    slug = models.SlugField(max_length=50, primary_key=True, unique=True, blank=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(ArtMedium, self).save(*args, **kwargs)


class ArtCommunity(models.Model):
    name = models.CharField(max_length=100, blank=False)
    description = models.TextField(max_length=500, blank=True, null=True)
    slug = models.SlugField(max_length=50, primary_key=True, unique=True, blank=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(ArtCommunity, self).save(*args, **kwargs)


class ArtGenre(models.Model):
    name = models.CharField(max_length=100, blank=False)
    description = models.TextField(max_length=500, blank=True, null=True)
    slug = models.SlugField(max_length=50, primary_key=True, unique=True, blank=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(ArtGenre, self).save(*args, **kwargs)


class Artist(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # institutuions = models.ManyToManyField(blank=True)
    # communities = models.ManyToManyField(blank=True)
    # mediums = models.ManyToManyField(blank=True)
    instagram = models.URLField(blank=True)
    twitter = models.URLField(blank=True)
    facebook = models.URLField(blank=True)
    bio = models.TextField(max_length=500, blank=True, null=True)
    slug = models.SlugField(max_length=50, primary_key=True, unique=True, blank=True)
    artist_image = models.ImageField(default='default_artist_image.jpg', upload_to='artist_images')
    art_mediums = models.ManyToManyField(ArtMedium, blank=True)
    art_communities = models.ManyToManyField(ArtCommunity, blank=True)
    art_genres = models.ManyToManyField(ArtGenre, blank=True)
    artist_headshot = models.ImageField(default='default_artist_headshot.jpg', upload_to='artist_headshots')
    studio_image = models.ImageField(default='default_artist_studio.jpg', upload_to='artist_studios')

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


# signal to detect if artitem was just approved, and if so, does the artist want it auto-for-sale? then do it!
# @receiver(pre_save, sender=ArtItem)
# def pre_artitem_saved_signal(sender, instance: ArtItem, **kwargs):
#     print('HERE COMES THE SIGNAL:pre_artitem_saved_signal')
#     print(sender, instance)
#     # get the model instance before the change
#     previous = sender.objects.get(slug=instance.slug)
#     new_version = instance.objects.get(slug=instance.slug)
#     print('print previous')
#     print(previous)
#     # check to see if this instance wants to be 'For Sale' once approved
#     if previous.publish_after_approved:
#         print('> here checked if the artist wants it approved')
#         # Check to see if new saved version will have approval status: approved
#         if sender.approval_status == 'Approved':
#             print('>> here checked if the new status is approved')
#             # check to see if the previous version of this instance wasn't already approved and that the art_status isnt already 'For Sale'
#             if previous.approval_status != 'Approved' & previous.art_status != 'For Sale':
#                 # switch new version of this instance from art_status draft to For Sale
#                 print('>>> Here will be the switch')





# def pre_artitem_created_signal(sender, instance, *args, **kwargs):
#     instance.slug = slugify(instance)


