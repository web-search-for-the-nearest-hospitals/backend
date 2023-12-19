from django.contrib import admin

from user.models import User


class BaseAdmin(admin.ModelAdmin):
    empty_value_display = "-пусто-"


@admin.register(User)
class UserAdmin(BaseAdmin):
    fields = (
        "username",
        "email",
        "role",
        "first_name",
        "last_name",
        "phone",
    )   
    search_fields = ("username", "role", "phone")
    list_filter = ("username",)
