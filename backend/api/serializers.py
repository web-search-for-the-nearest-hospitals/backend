from django.db import transaction
from django.shortcuts import get_object_or_404
from django.urls import reverse
from rest_framework import serializers

from organizations.models import (District,
                                  Organization, OrganizationSpecialty,
                                  OrganizationBusinessHour,
                                  Specialty, Town)


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


class TownSerializer(serializers.ModelSerializer):
    """Сериализатор города."""

    districts = serializers.SlugRelatedField(
        many=True, slug_field='name',
        read_only=True,
        help_text='Список районов города')

    class Meta:
        model = Town
        fields = ('name', 'districts', 'latitude', 'longitude')


class OrgBusinessHourCreateUpdateSerializer(serializers.ModelSerializer):
    """Сериализатор рабочих часов организации для POST & PATCH - методов."""

    class Meta:
        model = OrganizationBusinessHour
        fields = ('day', 'from_hour', 'to_hour')

    def validate(self, attrs):
        if attrs['from_hour'] > attrs['to_hour']:
            raise serializers.ValidationError(
                {"to_hour": "Время окончания рабочего дня не может быть"
                            " раньше времени начала рабочего дня"}
            )
        return super(
            OrgBusinessHourCreateUpdateSerializer, self).validate(attrs)


class OrgBusinessHourReadSerializer(serializers.ModelSerializer):
    """
    Сериализатор рабочих часов организации без required fields
    (для OPENAPI документации).
    """

    class Meta:
        model = OrganizationBusinessHour
        fields = ('day', 'from_hour', 'to_hour')
        extra_kwargs = {
            'day': {'required': False},
            'from_hour': {'required': False},
            'to_hour': {'required': False}
        }


class OrgSpecialtyCreateUpdateSerializer(serializers.ModelSerializer):
    """Сериализатор специальностей организации для POST & PATCH - методов."""

    code = serializers.CharField(source='specialty.code')
    name = serializers.CharField(source='specialty.name')
    skill = serializers.CharField(source='specialty.skill')

    class Meta:
        model = OrganizationSpecialty
        fields = ('code', 'name', 'skill', 'working_hours', 'day_of_the_week')


class OrgSpecialtyRetrieveSerializer(serializers.ModelSerializer):
    """Сериализатор специальностей организации для RETRIEVE-метода."""

    skill = serializers.CharField(
        source='specialty.skill',
        help_text='Специальность врача',
        required=False)

    class Meta:
        model = OrganizationSpecialty
        fields = ('skill',)


class OrganizationRetrieveSerializer(serializers.ModelSerializer):
    """Сериализатор организации для RETRIEVE-метода."""

    specialties = OrgSpecialtyRetrieveSerializer(
        read_only=True,
        many=True,
        help_text='Имеющиеся в организации специальности врачей')

    business_hours = OrgBusinessHourReadSerializer(
        many=True,
        read_only=True,
        help_text='Рабочие часы организации')

    class Meta:
        model = Organization
        lookup_field = 'uuid'
        fields = ('short_name', 'factual_address', 'site', 'about', 'phone',
                  'is_full_time', 'business_hours', 'specialties')
        extra_kwargs = {
            'short_name': {'required': False},
            'factual_address': {'required': False},
        }


class OrganizationListSerializer(serializers.ModelSerializer):
    """Сериализатор организации для LIST-метода."""

    relative_addr = serializers.SerializerMethodField(
        label='relative_addr',
        help_text='Относительный адрес организации в сервисе',
        read_only=True)

    town = serializers.SlugRelatedField(
        slug_field='name',
        help_text='Город расположения организации',
        read_only=True
    )

    district = serializers.SlugRelatedField(
        slug_field='name',
        help_text='Район расположения организации',
        read_only=True
    )

    business_hours = OrgBusinessHourReadSerializer(
        many=True,
        read_only=True,
        help_text='Рабочие часы организации')

    class Meta:
        model = Organization
        fields = ('relative_addr', 'short_name', 'factual_address',
                  'longitude', 'latitude', 'site', 'about', 'phone', 'town',
                  'district', 'is_full_time', 'business_hours')
        extra_kwargs = {
            'short_name': {'required': False},
            'factual_address': {'required': False},
            'longitude': {'required': False},
            'latitude': {'required': False},
        }

    def get_relative_addr(self, obj):
        return reverse('api:organizations-detail',
                       kwargs={'uuid': obj.uuid})


class OrganizationCreateUpdateSerializer(serializers.ModelSerializer):
    """Сериализатор организации для CREATE & UPDATE."""

    specialties = OrgSpecialtyCreateUpdateSerializer(many=True, required=False)

    relative_addr = serializers.SerializerMethodField(
        label='relative_addr',
        help_text='Относительный адрес организации в сервисе',
        read_only=True)

    town = serializers.SlugRelatedField(
        queryset=Town.objects.all(),
        slug_field='name',
        help_text='Город расположения организации'
    )

    district = serializers.SlugRelatedField(
        queryset=District.objects.all(),
        slug_field='name',
        help_text='Район расположения организации'
    )

    business_hours = OrgBusinessHourCreateUpdateSerializer(
        many=True,
        help_text='Рабочие часы организации')

    class Meta:
        model = Organization
        lookup_field = 'uuid'
        fields = ('relative_addr', 'short_name', 'factual_address',
                  'longitude', 'latitude', 'site', 'is_gov', 'is_full_time',
                  'about', 'phone', 'town', 'district', 'business_hours',
                  'specialties')

    def get_relative_addr(self, obj):
        return reverse('api:organizations-detail',
                       kwargs={'uuid': obj.uuid})

    @staticmethod
    def create_org_specialty(specialties: dict,
                             org: Organization) -> None:
        new_org_specialties = []

        for specialty in specialties:
            spec_data = specialty['specialty']
            code = spec_data['code']
            name = spec_data['name']
            skill = spec_data['skill']
            working_hours = specialty['working_hours']
            day_of_the_week = specialty['day_of_the_week']
            current_specialty = get_object_or_404(
                Specialty, code=code,
                name=name, skill=skill)
            new_org_specialties.append(
                OrganizationSpecialty(
                    organization=org,
                    specialty=current_specialty,
                    working_hours=working_hours,
                    day_of_the_week=day_of_the_week
                )
            )
        OrganizationSpecialty.objects.bulk_create(new_org_specialties)

    @staticmethod
    def create_org_business_hours(business_hours: dict,
                                  org: Organization) -> None:
        new_org_business_hours = [
            OrganizationBusinessHour(
                day=hour['day'],
                from_hour=hour['from_hour'],
                to_hour=hour['to_hour'],
                organization=org) for hour in business_hours
        ]
        OrganizationBusinessHour.objects.bulk_create(new_org_business_hours)

    def create(self, validated_data):
        specialties = validated_data.pop('specialties')
        business_hours = validated_data.pop('business_hours')

        with transaction.atomic():
            org = Organization.objects.create(**validated_data)
            self.create_org_specialty(specialties, org)
            self.create_org_business_hours(business_hours, org)
        return org

    def update(self, instance, validated_data):
        specialties = validated_data.pop('specialties')
        business_hours = validated_data.pop('business_hours')

        with transaction.atomic():
            instance = super().update(instance, validated_data)
            OrganizationSpecialty.objects.filter(
                organization=instance
            ).delete()
            self.create_org_specialty(specialties, instance)
            OrganizationBusinessHour.objects.filter(
                organization=instance
            ).delete()
            self.create_org_business_hours(business_hours, instance)
        return instance
