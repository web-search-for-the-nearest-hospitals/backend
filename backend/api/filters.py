import django_filters
from django_filters import rest_framework as filters
from rest_framework import filters as default_filters

from organizations.models import Organization


class SearchFilterWithCustomDescription(default_filters.SearchFilter):
    search_title = 'Поиск'
    search_description = 'Поиск по полному и сокращенному наименованиям'


class NumberInFilter(django_filters.BaseInFilter,
                     django_filters.NumberFilter):
    pass


class OrgFilter(filters.FilterSet):
    """Фильтр по свойствам организаций."""

    specialties = django_filters.CharFilter(
        lookup_expr="exact",
        field_name='specialties__specialty__name',
        label='Фильтр по наличию специальностей'
    )

    districts = NumberInFilter(
        lookup_expr='in',
        field_name='district__id',
        label='Фильтр по районам <IN [ARRAY]>'
    )

    is_gov = django_filters.BooleanFilter(
        label='Фильтр по государственным и негосударственным организациям'
    )

    class Meta:
        model = Organization
        fields = ['specialties', 'districts', 'is_gov']
