from rest_framework import serializers

from .models import District


class DistrictField(serializers.CharField):
    """Костылька для корректного отображения района.
    (Почти велосипед к RelatedField, но зато есть валидация
    с учетом значения поля <town>).
    """

    def to_representation(self, value):
        if isinstance(value, District):
            return value.name
        return str(value)
