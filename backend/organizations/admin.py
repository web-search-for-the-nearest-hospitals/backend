from django.contrib import admin
from django.contrib.auth.models import Group, User

from .models import Organization


@admin.register(Organization)
class OrganizationAdminModel(admin.ModelAdmin):
    """Модель админки для организаций."""

    list_display = ('full_name', 'short_name', 'inn', 'factual_address')
    search_fields = ('inn__exact',)


admin.site.unregister(User)
admin.site.unregister(Group)
