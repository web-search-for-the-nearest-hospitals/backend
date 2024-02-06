from django.contrib import admin

from .models import District, Town


@admin.register(District)
class DistrictAdminModel(admin.ModelAdmin):
    """Модель админки для района."""

    list_display = ('name', 'town', 'longitude', 'latitude')


@admin.register(Town)
class TownAdminModel(admin.ModelAdmin):
    """Модель админки для города."""

    list_display = ('name', 'longitude', 'latitude')
