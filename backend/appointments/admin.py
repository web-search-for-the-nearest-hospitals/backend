from django.contrib import admin

from .models import Appointment


@admin.register(Appointment)
class AppointmentAdminModel(admin.ModelAdmin):
    """Модель админки для записи к врачу."""

    list_display = ('id', 'organization', 'specialty', 'client',
                    'datetime_start', 'status')
