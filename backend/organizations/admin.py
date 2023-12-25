from django.contrib import admin

from .models import (Organization, OrganizationSpecialty, Specialty, Town,
                     District, OrganizationBusinessHour)


class BusinessHourInline(admin.StackedInline):
    model = OrganizationBusinessHour
    extra = 7


@admin.register(Organization)
class OrganizationAdminModel(admin.ModelAdmin):
    """Модель админки для организаций."""

    list_display = ('full_name', 'short_name', 'inn', 'factual_address',
                    'date_added', 'longitude', 'latitude', 'uuid')
    search_fields = ('inn__exact',)
    inlines = [BusinessHourInline, ]


@admin.register(Specialty)
class SpecialtyAdminModel(admin.ModelAdmin):
    """Модель админки для специальностей врачей."""

    list_display = ('code', 'name', 'skill')


@admin.register(OrganizationSpecialty)
class OrganizationSpecialtyAdminModel(admin.ModelAdmin):
    """Модель админки для расписания специальностей в больничке."""

    list_display = ('organization', 'specialty', 'working_hours',
                    'day_of_the_week')


@admin.register(Town)
class TownAdminModel(admin.ModelAdmin):
    """Модель админки для города."""

    list_display = ('name', 'longitude', 'latitude')


@admin.register(District)
class DistrictAdminModel(admin.ModelAdmin):
    """Модель админки для района."""

    list_display = ('name', 'town')
