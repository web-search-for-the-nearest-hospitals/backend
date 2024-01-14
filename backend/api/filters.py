import django_filters
from rest_framework import filters

from organizations.models import Organization
from .utils import count_distance


class SearchFilterWithCustomDescription(filters.SearchFilter):
    search_title = 'Поиск'
    search_description = 'Поиск по сокращенному наименованию организации'


class NumberFilterWOFilter(django_filters.NumberFilter):
    """Фильтр, но не фильтр =)
    Забираем валидацию поля без фильтрации по нему."""

    def filter(self, qs, value):
        if value in ([], (), {}, "", None):
            return qs
        if self.distinct:
            return qs.distinct()
        return qs


class OrgFilter(django_filters.FilterSet):
    """Фильтр по свойствам организаций."""

    specialty = django_filters.CharFilter(
        lookup_expr="exact",
        field_name='specialties__specialty_id',
        label='Фильтр по коду специальности врача',
        distinct=True
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

    lat = NumberFilterWOFilter(
        label='Значение широты для фильтрации',
        field_name='latitude'
    )

    long = NumberFilterWOFilter(
        label='Значение долготы для фильтрации',
        field_name='longitude'
    )

    def filter_queryset(self, queryset):
        """Добавляем фильтрацию по удаленности организаций
        от переданных координат широты и долготы."""

        qs = super().filter_queryset(queryset)
        lat = self.form.cleaned_data.get('lat') or 54.51367
        long = self.form.cleaned_data.get('long') or 36.26134
        return (
            qs
            .annotate(distance=count_distance(long, lat))
            .order_by('distance')
        )

    class Meta:
        model = Organization
        fields = ['specialty', 'town', 'district', 'is_gov', 'is_full_time',
                  'lat', 'long']
