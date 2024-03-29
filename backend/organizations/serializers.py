import re

from django.core.exceptions import ObjectDoesNotExist
from django.db import transaction
from django.http import Http404
from django.shortcuts import get_object_or_404
from django.urls import reverse
from rest_framework import serializers, validators

from geography.fields import DistrictField
from geography.models import District, Town
from specialties.models import Specialty
from .fields import SlugRelatedFieldWith404
from .models import (Organization, OrganizationSpecialty,
                     OrganizationBusinessHour)
from .utils import PHONE_NUMBER_REGEX, dist_to_str, haversine


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

    code = serializers.CharField(
        source='specialty.code',
        help_text='Код специальности врача')

    class Meta:
        model = OrganizationSpecialty
        fields = ('code', 'day_of_the_week', 'from_hour', 'to_hour')

    def validate(self, attrs):
        if attrs['from_hour'] > attrs['to_hour']:
            raise serializers.ValidationError(
                {"to_hour": "Время окончания рабочего дня не может быть"
                            " раньше времени начала рабочего дня"}
            )
        return super(
            OrgSpecialtyCreateUpdateSerializer, self).validate(attrs)


class OrgSpecialtyRetrieveSerializer(serializers.ModelSerializer):
    """Сериализатор специальностей организации для RETRIEVE-метода."""

    skill = serializers.CharField(
        source='specialty.skill',
        help_text='Специальность врача',
        required=False)

    code = serializers.CharField(
        source='specialty.code',
        help_text='Код специальности',
        required=False)

    class Meta:
        model = OrganizationSpecialty
        fields = ('skill', 'code')


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

    rating = serializers.FloatField(
        min_value=0.0,
        max_value=5.0,
        help_text='Рейтинг организации (либо Float, либо null)',
        required=False)

    class Meta:
        model = Organization
        lookup_field = 'uuid'
        fields = ('short_name', 'factual_address', 'site', 'about', 'phone',
                  'is_full_time', 'rating', 'business_hours', 'specialties')
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
        read_only=True)

    district = serializers.SlugRelatedField(
        slug_field='name',
        help_text='Район расположения организации',
        read_only=True)

    business_hours = OrgBusinessHourReadSerializer(
        many=True,
        read_only=True,
        help_text='Рабочие часы организации')

    distance = serializers.SerializerMethodField(
        help_text='Форматированное расстояние до организации')

    can_appoint = serializers.SerializerMethodField(
        help_text='Можно ли записаться в организацию на прием к врачу'
    )

    rating = serializers.FloatField(
        min_value=0.0,
        max_value=5.0,
        help_text='Рейтинг организации (либо Float, либо null)',
        required=False)

    class Meta:
        model = Organization
        fields = ('relative_addr', 'short_name', 'factual_address',
                  'longitude', 'latitude', 'site', 'about', 'phone', 'town',
                  'district', 'is_full_time', 'distance', 'can_appoint',
                  'rating', 'business_hours',
                  )
        extra_kwargs = {
            'short_name': {'required': False},
            'factual_address': {'required': False},
            'longitude': {'required': False},
            'latitude': {'required': False}
        }

    def get_relative_addr(self, obj) -> str:
        return reverse('api:organizations-detail',
                       kwargs={'uuid': obj.uuid})

    def get_distance(self, obj) -> str:
        return dist_to_str(obj.distance)

    def get_can_appoint(self, obj) -> bool:
        return obj.specialties.exists()


class OrganizationCreateUpdateSerializer(serializers.ModelSerializer):
    """Сериализатор организации для CREATE & UPDATE."""

    specialties = OrgSpecialtyCreateUpdateSerializer(
        many=True,
        required=False,
        help_text='Специальности врачей, работающих в организации')

    relative_addr = serializers.SerializerMethodField(
        label='relative_addr',
        help_text='Относительный адрес организации в сервисе',
        read_only=True)

    town = SlugRelatedFieldWith404(
        queryset=Town.objects.all(),
        slug_field='name',
        help_text='Город расположения организации')

    district = DistrictField(
        required=True,
        help_text='Район расположения организации')

    business_hours = OrgBusinessHourCreateUpdateSerializer(
        many=True,
        help_text='Рабочие часы организации')

    owner = serializers.HiddenField(
        default=serializers.CurrentUserDefault())

    class Meta:
        model = Organization
        lookup_field = 'uuid'
        fields = ('relative_addr', 'short_name', 'factual_address',
                  'longitude', 'latitude', 'site', 'is_gov', 'is_full_time',
                  'about', 'phone', 'town', 'district', 'business_hours',
                  'specialties', 'owner')
        validators = [
            validators.UniqueTogetherValidator(
                queryset=Organization.objects.all(),
                fields=['short_name', 'factual_address']
            )
        ]

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
            day_of_the_week = specialty['day_of_the_week']
            from_hour = specialty['from_hour']
            to_hour = specialty['to_hour']
            current_specialty = get_object_or_404(Specialty, code=code)
            new_org_specialties.append(
                OrganizationSpecialty(
                    organization=org,
                    specialty=current_specialty,
                    day_of_the_week=day_of_the_week,
                    from_hour=from_hour,
                    to_hour=to_hour
                )
            )
        OrganizationSpecialty.objects.bulk_create(new_org_specialties)

    def validate(self, attrs):

        validated_data = super().validate(attrs)

        district = validated_data.pop('district')
        town = validated_data.get('town')

        is_full_time = validated_data.get('is_full_time')
        business_hours = validated_data.get('business_hours')

        errors = dict()

        if haversine(
                town.longitude,
                town.latitude,
                validated_data.get('longitude'),
                validated_data.get('latitude')
        ) > Town.MAX_DIST:
            errors['latitude & longitude'] = (f'Организация слишком далеко '
                                              f'расположена от центра города'
                                              f' (больше допустимых'
                                              f' {Town.MAX_DIST} километров).')

        if is_full_time and business_hours:
            errors['is_full_time & business_hours'] = ('Организация либо '
                                                       'круглосуточная, '
                                                       'либо по графику')

        if not is_full_time and not business_hours:
            errors['is_full_time & business_hours'] = ('Нет информации о '
                                                       'графике работы '
                                                       'организации')

        if errors:
            raise serializers.ValidationError(errors)

        try:
            validated_data['district'] = (
                District
                .objects
                .only('id')
                .get(town=town, name=district)
            )

        except ObjectDoesNotExist:
            raise Http404
        return validated_data

    def validate_phone(self, value):
        if not re.match(PHONE_NUMBER_REGEX, value):
            raise serializers.ValidationError(
                'Номер телефона не соответствует шаблону'
            )

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
