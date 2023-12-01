from rest_framework import serializers

from organizations.models import Organization


class OrganizationListSerializer(serializers.ModelSerializer):
    """Сериализатор для списка организации."""

    class Meta:
        model = Organization
        exclude = ['id', 'date_added', 'region_code']
        read_only_fields = ('full_name',)


class OrganizationRetrieveSerializer(serializers.ModelSerializer):
    """Сериализатор для профиля организации."""

    class Meta:
        model = Organization
        exclude = ['id', 'date_added']
        read_only_fields = ('full_name', 'factual_address')


class ErrorSerializer(serializers.Serializer):
    """Сериализатор для вывода ошибки."""

    detail = serializers.CharField(help_text='Описание ошибки',
                                   required=False)
