from django.contrib import admin

from .models import (Organization,
                     OrganizationSpecialty, OrganizationBusinessHour)


class BusinessHourInline(admin.StackedInline):
    """Встраиваемая модель админки для рабочих часов организации."""

    model = OrganizationBusinessHour
    extra = 7


@admin.register(Organization)
class OrganizationAdminModel(admin.ModelAdmin):
    """Модель админки для организаций."""

    list_display = ('short_name', 'factual_address',
                    'date_added', 'longitude', 'latitude', 'uuid')
    inlines = [BusinessHourInline, ]


@admin.register(OrganizationSpecialty)
class OrganizationSpecialtyAdminModel(admin.ModelAdmin):
    """Модель админки для расписания специальностей в больничке."""

    list_display = ('organization', 'specialty',
                    'day_of_the_week', 'from_hour', 'to_hour')
    ordering = ['organization', 'day_of_the_week', 'from_hour']
    list_filter = ('day_of_the_week',)
