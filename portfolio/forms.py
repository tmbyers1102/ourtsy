from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, UsernameField
from .models import ArtItem


User = get_user_model()


class ArtModelForm(forms.ModelForm):
    class Meta:
        model = ArtItem
        fields = (
            'title',
            'price'
        )


class ArtForm(forms.Form):
    title = forms.CharField()


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ("username",)
        field_classes = {'username': UsernameField}