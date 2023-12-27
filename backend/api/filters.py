import django_filters
from django_filters import rest_framework as filters
from rest_framework import filters as default_filters

from organizations.models import Organization


class SearchFilterWithCustomDescription(default_filters.SearchFilter):
    search_title = 'Поиск'
    search_description = 'Поиск по сокращенному наименованию организации'


class OrgFilter(filters.FilterSet):
    """Фильтр по свойствам организаций."""

    specialty = django_filters.CharFilter(
        lookup_expr="exact",
        field_name='specialties__specialty__skill',
        label='Фильтр по специальности врача'
    )

    district = django_filters.CharFilter(
        lookup_expr='exact',
        field_name='district__name',
        label='Фильтр по названию района расположения организации'
    )

    town = django_filters.CharFilter(
        lookup_expr='exact',
        field_name='town__name',
        label='Фильтр по названию города расположения организации'
    )

    is_gov = django_filters.BooleanFilter(
        label='Фильтр по государственным и негосударственным организациям',
        field_name='is_gov'
    )

    is_full_time = django_filters.BooleanFilter(
        label='Фильтр по круглосуточным организациям',
        field_name='is_full_time'
    )

    class Meta:
        model = Organization
        fields = ['specialty', 'town', 'district', 'is_gov', 'is_full_time']
