from django.forms.widgets import CheckboxInput, CheckboxSelectMultiple, TextInput, Widget, DateInput
import django_filters
from django_filters import CharFilter, ModelChoiceFilter, DateFilter, DateFromToRangeFilter
from django_filters.widgets import RangeWidget
from datetime import datetime, timedelta

from .models import *


class ArtSubmissionsFilter(django_filters.FilterSet):
    title = CharFilter(field_name="title", lookup_expr="icontains", widget=TextInput(attrs={'placeholder': 'Search a title'}))
    start_date = DateFilter(widget=DateInput(attrs={'size': 4, 'type': 'date'}), field_name="date_submitted", lookup_expr="gte")
    end_date = DateFilter(widget=DateInput(attrs={'size': 4, 'type': 'date', 'placeholder': 'fff'}), field_name="date_submitted", lookup_expr="lte")
    # date_range = django_filters.DateFromToRangeFilter()
    approval_status_id = django_filters.ModelMultipleChoiceFilter(
        queryset=ApprovalStatus.objects.all(),
        widget=CheckboxSelectMultiple,
    )
    # urgent_review = django_filters.ModelMultipleChoiceFilter(
    #     queryset=ArtItem.objects.all(),
    #     widget=CheckboxSelectMultiple,
    # )
    class Meta:
        model = ArtItem
        fields = [
            'urgent_review',
            'title',
            'approval_status',
        ]
        exclude = [
            'date_submitted',
        ]


class ArtFilter(django_filters.FilterSet):
    # this area is for type-in fields so it can be a partial match
    # title = CharFilter(field_name="title", lookup_expr="icontains")
    # tags = CharFilter(field_name="tags__name", lookup_expr="icontains")
    # artist = CharFilter(field_name="artist", lookup_expr="icontains")
    art_mediums = django_filters.ModelMultipleChoiceFilter(
        queryset=ArtMedium.objects.all(),
        widget=CheckboxSelectMultiple,
    )
    art_communities = django_filters.ModelMultipleChoiceFilter(
        queryset=ArtCommunity.objects.all(),
        widget=CheckboxSelectMultiple,
    )
    art_genres = django_filters.ModelMultipleChoiceFilter(
        queryset=ArtGenre.objects.all(),
        widget=CheckboxSelectMultiple,
    )
    price = django_filters.ModelMultipleChoiceFilter(
        queryset=ArtItem.objects.values_list('price', flat=True).distinct(),
        widget=CheckboxSelectMultiple,
    )

    class Meta:
        model = ArtItem
        # for drop down fields --such as pre-set genres or mediums-- just add here
        fields = [
            # 'art_mediums',
        ]


class ArtTagFilter(django_filters.FilterSet):
    object_id = CharFilter(field_name="object_id", lookup_expr="icontains")

    class Meta:
        model = GenericStringTaggedItem
        fields = [
        ]


class ArtMediumFilter(django_filters.FilterSet):
    pass