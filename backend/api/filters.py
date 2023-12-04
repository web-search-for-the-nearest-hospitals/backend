import django_filters
from django_filters import rest_framework as filters
from rest_framework import filters as default_filters

from organizations.models import Organization


class SearchFilterWithCustomDescription(default_filters.SearchFilter):
    search_title = 'Поиск'
    search_description = 'Параметр поиска по ИНН'


class SpecialtyFilter(filters.FilterSet):
    specialties = django_filters.CharFilter(
        lookup_expr="exact",
        field_name='specialties__specialty__name')

    class Meta:
        model = Organization
        fields = ['specialties']
