from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, UsernameField
from .models import ArtItem, Post
from taggit.forms import TagWidget


User = get_user_model()


class ArtModelForm(forms.ModelForm):
    class Meta:
        model = ArtItem
        fields = (
            'title',
            'price',
            'cover_image',
            'tags',
        )


class ArtForm(forms.Form):
    title = forms.CharField()


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ("username",)
        field_classes = {'username': UsernameField}


class ArtistForm(forms.Form):
    pass


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = [
            'title',
            'description',
        ]


