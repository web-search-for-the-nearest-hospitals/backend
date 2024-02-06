from django.contrib import admin

from reviews.models import Review


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'organization',
        'text',
        'author',
        'score',
        'pub_date',
    )
    search_fields = ('organization', 'author', 'pud_date',)
    list_filter = ('pub_date',)
    empty_value_display = '-пусто-'
