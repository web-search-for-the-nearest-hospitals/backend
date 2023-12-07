import django_filters
from django_filters import rest_framework as filters
from rest_framework import filters as default_filters

from organizations.models import Organization


class SearchFilterWithCustomDescription(default_filters.SearchFilter):
    search_title = 'Поиск'
    search_description = 'Параметр поиска по ИНН'


class NumberInFilter(django_filters.BaseInFilter, django_filters.NumberFilter):
    pass


class OrgFilter(filters.FilterSet):
    specialties = django_filters.CharFilter(
        lookup_expr="exact",
        field_name='specialties__specialty__name')

    districts = NumberInFilter(field_name='district__id', lookup_expr='in')

    class Meta:
        model = Organization
        fields = ['specialties', 'districts', 'is_gov']
