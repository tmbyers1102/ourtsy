from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, UsernameField
from django.forms import widgets
from .models import ArtImage, ArtItem, ArtMedium, Post
from taggit.forms import TagWidget
from django.forms.widgets import CheckboxSelectMultiple, Widget


User = get_user_model()



# this gathers all the mediums from the ArtMedium model
# MEDIUM_CHOICES = ([(x.name, x.name) for x in ArtMedium.objects.all()])


class ArtModelForm(forms.ModelForm):
    # art_mediums = forms.MultipleChoiceField(
    #     required=True,
    #     label='Art Mediums',
    #     widget=CheckboxSelectMultiple(),
    #     choices=MEDIUM_CHOICES
    # )
    class Meta:
        model = ArtItem
        fields = (
            'title',
            'price',
            'cover_image',
            'tags',
            'art_story',
            'art_mediums',
            'art_communities',
            'art_genres',
            'publish_after_approved',
        )
        widgets = {
            'art_mediums': forms.CheckboxSelectMultiple,
            'art_communities': forms.CheckboxSelectMultiple,
            'art_genres': forms.CheckboxSelectMultiple,
        }


class ArtImageUpdateForm(forms.ModelForm):
    class Meta:
        model = ArtImage
        fields = (
            'art_item',
            'image'
        )


class ArtUpdateModelForm(forms.ModelForm):
    # art_mediums = forms.MultipleChoiceField(
    #     required=True,
    #     label='Art Mediums',
    #     widget=CheckboxSelectMultiple(),
    #     choices=MEDIUM_CHOICES
    # )
    class Meta:
        model = ArtItem
        fields = (
            'title',
            'price',
            'cover_image',
            'tags',
            'art_story',
            'art_mediums',
            'art_communities',
            'art_genres',
            'art_status',
            'publish_after_approved',
            'review_note',
            'approval_status',
            'reviewed_by',
            'slug',
        )
        widgets = {
            'art_mediums': forms.CheckboxSelectMultiple,
            'art_communities': forms.CheckboxSelectMultiple,
            'art_genres': forms.CheckboxSelectMultiple,
        }


class ArtReviewModelForm(forms.ModelForm):
    class Meta:
        model = ArtItem
        fields = (
            'reviewed_by',
            'review_note',
            'approval_status',
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
            'text',
            'post_image',
        ]

    def clean(self):
        cleaned_data = super(PostForm, self).clean()
        text = cleaned_data.get('text')
        title = cleaned_data.get('title')
        if Post.objects.filter(title=self.cleaned_data['title']).exists():
            raise forms.ValidationError('This title is already taken. Please adjust!')
        if len(text) < 1500:
            self.add_error(
                'text', 'Posts must be 1500 characters or longer. Please add more text!'
            )
        if len(title) < 5:
            self.add_error(
                'text', 'The title must be 5 characters or longer. Please add more text!'
            )
        
        return self.cleaned_data
