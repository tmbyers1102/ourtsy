from portfolio.models import Artist
from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, UsernameField
from .models import Lead, Agent

User = get_user_model()


class LeadModelForm(forms.ModelForm):
    class Meta:
        model = Lead
        fields = (
            'first_name',
            'last_name',
            'age',
            'agent',
        )

class LeadForm(forms.Form):
    first_name = forms.CharField()
    last_name = forms.CharField()
    age = forms.IntegerField(min_value=0)


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ("username",)
        field_classes = {'username': UsernameField}


class AssignAgentForm(forms.Form):
    agent = forms.ModelChoiceField(queryset=Agent.objects.none())

    def __init__(self, *args, **kwargs):
        request = kwargs.pop("request")
        agents = Agent.objects.filter(organization=request.user.userprofile)
        super(AssignAgentForm, self).__init__(*args, **kwargs)
        self.fields["agent"].queryset = agents


class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        # when submitted updates ...user
        model = User
        # these are the fields we want on our form
        fields = [
            'email',
            'first_name',
            'last_name',
            'twitter_name',
            'twitter_url',
            'instagram_name',
            'instagram_url',
            'facebook_name',
            'facebook_url',
        ]


class ArtistUpdateForm(forms.ModelForm):
    class Meta:
        model = Artist
        fields = [
            'bio',
            'art_mediums',
            'art_communities',
            'art_genres',
        ]
        widgets = {
            'art_mediums': forms.CheckboxSelectMultiple,
            'art_communities': forms.CheckboxSelectMultiple,
            'art_genres': forms.CheckboxSelectMultiple,
        }