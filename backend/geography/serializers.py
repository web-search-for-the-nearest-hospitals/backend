from django.urls import reverse
from rest_framework import serializers

from .models import Town, District


class DistrictSerializer(serializers.ModelSerializer):
    """Сериализатор административного района."""

    class Meta:
        model = District
        fields = ('name', 'latitude', 'longitude')
        extra_kwargs = {
            'name': {'required': False},
            'latitude': {'required': False},
            'longitude': {'required': False}
        }


class TownRetrieveSerializer(serializers.ModelSerializer):
    """Сериализатор города для метода GET (RETRIEVE)."""

    districts = DistrictSerializer(
        many=True,
        read_only=True,
        help_text='Список районов города')

    class Meta:
        model = Town
        fields = ('name', 'latitude', 'longitude', 'districts')
        extra_kwargs = {
            'name': {'required': False},
            'latitude': {'required': False},
            'longitude': {'required': False}
        }


class TownListSerializer(serializers.ModelSerializer):
    """Сериализатор города для метода GET (LIST)."""

    relative_addr = serializers.SerializerMethodField(
        label='relative_addr',
        help_text='Относительный адрес города в сервисе',
        read_only=True)

    class Meta:
        model = Town
        fields = ('name', 'relative_addr')
        extra_kwargs = {
            'name': {'required': False}
        }

    def get_relative_addr(self, obj):
        return reverse('api:towns-detail',
                       kwargs={'pk': obj.pk})
