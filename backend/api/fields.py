from rest_framework import serializers
from django.shortcuts import get_object_or_404

from organizations.models import District


class DistrictField(serializers.CharField):
    """Костылька для корректного отображения района.
    (Почти велосипед к RelatedField, но зато есть валидация
    с учетом значения поля <town>).
    """

    def to_representation(self, value):
        if isinstance(value, District):
            return value.name
        return str(value)


class SlugRelatedFieldWith404(serializers.SlugRelatedField):

    def to_internal_value(self, data):
        queryset = self.get_queryset()
        return get_object_or_404(queryset.filter(**{self.slug_field: data}))
