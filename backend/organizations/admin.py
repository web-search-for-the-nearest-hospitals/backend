from django.contrib import admin

from .models import Organization, OrganizationSpecialty, Specialty


@admin.register(Organization)
class OrganizationAdminModel(admin.ModelAdmin):
    """Модель админки для организаций."""

    list_display = ('full_name', 'short_name', 'inn', 'factual_address',
                    'date_added', 'longitude', 'latitude')
    search_fields = ('inn__exact',)


@admin.register(Specialty)
class SpecialtyAdminModel(admin.ModelAdmin):
    """Модель админки для специальностей врачей."""

    list_display = ('code', 'name', 'skill')


@admin.register(OrganizationSpecialty)
class OrganizationSpecialtyAdminModel(admin.ModelAdmin):
    """Модель админки для расписания специальностей в больничке."""

    list_display = ('organization', 'specialty', 'working_hours',
                    'day_of_the_week')
