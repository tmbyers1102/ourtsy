import django_filters
from django_filters import CharFilter, ModelChoiceFilter

from .models import *


class ArtFilter(django_filters.FilterSet):
    # this area is for type-in fields so it can be a partial match
    title = CharFilter(field_name="title", lookup_expr="icontains")
    tags = CharFilter(field_name="tags__name", lookup_expr="icontains")
    artist = CharFilter(field_name="artist", lookup_expr="icontains")

    class Meta:
        model = ArtItem
        # for drop down fields --such as pre-set genres or mediums-- just add here
        fields = [
            # 'artist',
        ]


class ArtTagFilter(django_filters.FilterSet):
    object_id = CharFilter(field_name="object_id", lookup_expr="icontains")

    class Meta:
        model = GenericStringTaggedItem
        fields = [
        ]