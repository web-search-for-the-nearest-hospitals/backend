from rest_framework import serializers

from organizations.models import Organization, Specialty


class OrganizationListSerializer(serializers.ModelSerializer):
    """Сериализатор для списка организации."""

    class Meta:
        model = Organization
        exclude = ['id', 'date_added', 'region_code']


class OrganizationRetrieveSerializer(serializers.ModelSerializer):
    """Сериализатор для профиля организации."""

    class Meta:
        model = Organization
        exclude = ['id', 'date_added']


class SpecialtySerializer(serializers.ModelSerializer):
    """Сериализатор для специальности врача."""

    class Meta:
        model = Specialty
        fields = ('code', 'name', 'skill')


class ErrorSerializer(serializers.Serializer):
    """Сериализатор для вывода ошибки."""

    detail = serializers.CharField(help_text='Описание ошибки',
                                   required=False)
