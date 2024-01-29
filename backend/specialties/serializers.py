from rest_framework import serializers

from .models import Specialty


class SpecialtySerializer(serializers.ModelSerializer):
    """Сериализатор специальности врача."""

    class Meta:
        model = Specialty
        fields = ('code', 'name', 'skill')
        extra_kwargs = {
            'code': {'required': False},
            'name': {'required': False},
            'skill': {'required': False}
        }
