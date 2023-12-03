from rest_framework import serializers

from organizations.models import (Organization, OrganizationSpecialty,
                                  Specialty)


class SpecialtySerializer(serializers.ModelSerializer):
    """Сериализатор для специальности врача."""

    class Meta:
        model = Specialty
        fields = ('code', 'name', 'skill')


class ScheduleOrgListSerializer(serializers.ModelSerializer):
    """Сериализатор для отображения специальностей списка организаций."""

    name = serializers.ReadOnlyField(source='specialty.name')
    code = serializers.ReadOnlyField(source='specialty.code')

    class Meta:
        model = OrganizationSpecialty
        fields = ('name', 'code')


class ScheduleOrgRetrieveSerializer(serializers.ModelSerializer):
    """Сериализатор для отображения специальностей организации."""

    name = serializers.ReadOnlyField(source='specialty.name')
    code = serializers.ReadOnlyField(source='specialty.code')
    skill = serializers.ReadOnlyField(source='specialty.skill')

    class Meta:
        model = OrganizationSpecialty
        fields = ('code', 'name', 'skill', 'working_hours',
                  'day_of_the_week')


class OrganizationListSerializer(serializers.ModelSerializer):
    """Сериализатор для списка организации."""

    specialties = ScheduleOrgListSerializer(many=True)

    class Meta:
        model = Organization
        fields = ('id', 'full_name', 'short_name', 'factual_address',
                  'longitude', 'latitude', 'site', 'specialties')


class OrganizationRetrieveSerializer(serializers.ModelSerializer):
    """Сериализатор для профиля организации."""

    specialties = ScheduleOrgRetrieveSerializer(many=True)

    class Meta:
        model = Organization
        fields = ('full_name', 'short_name',
                  'inn', 'date_added', 'factual_address',
                  'region_code', 'longitude', 'latitude',
                  'site', 'email', 'specialties')


class ErrorSerializer(serializers.Serializer):
    """Сериализатор для вывода ошибки."""

    detail = serializers.CharField(help_text='Описание ошибки',
                                   required=False)
