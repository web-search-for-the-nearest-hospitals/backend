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
        "third_name",
        "phone",
        "date_of_birth"
    )
    list_display = ("email", "last_name", "first_name", "role")

    search_fields = ("username", "role", "phone")
