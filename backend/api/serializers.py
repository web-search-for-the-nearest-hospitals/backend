import datetime
import re

from django.core.exceptions import ObjectDoesNotExist
from django.core.validators import RegexValidator
from django.db import transaction
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.contrib.auth.hashers import make_password
from rest_framework import serializers, validators

from organizations.models import (Appointment, District,
                                  Organization, OrganizationSpecialty,
                                  OrganizationBusinessHour,
                                  Specialty, Town)
from user.models import User


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

    code = serializers.CharField(source='specialty.code',
                                 help_text='Специальность врача')

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
        read_only=True)

    district = serializers.SlugRelatedField(
        slug_field='name',
        help_text='Район расположения организации',
        read_only=True)

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
        queryset=Town.objects.only('id').all(),
        slug_field='name',
        help_text='Город расположения организации')

    district = serializers.CharField(
        required=True,
        help_text='Район расположения организации')

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

        try:
            validated_data['district'] = (
                District
                .objects
                .only('id')
                .get(town=town, name=district)
            )
        except ObjectDoesNotExist:
            raise serializers.ValidationError(
                {"district": f"Объект с name={district} не существует."})
        return validated_data

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


class AppointmentParamSerializer(serializers.Serializer):
    """Сериализатор параметров запроса свободных временных окошек записи
    к врачу организации."""

    spec_code = serializers.CharField(
        required=True,
        help_text='Код специальности врача для приема',
        validators=[RegexValidator(regex=r'3[123]-08-\d\d')])

    which_date = serializers.DateField(
        required=True,
        help_text='Дата приема')

    def validate_which_date(self, value):
        if datetime.date.today() > value:
            raise serializers.ValidationError(
                "Дата записи не может быть позднее сегодняшней.")
        if datetime.date.today() + datetime.timedelta(days=15) < value:
            raise serializers.ValidationError(
                "Записи не формируются более 15-ти дней вперед.")
        return value


class AppointmentListSerializer(serializers.ModelSerializer):
    """Сериализатор параметров запроса свободных временных окошек записи
    к врачу организации."""

    id = serializers.IntegerField(
        help_text='ID талона на запись',
        required=False)

    datetime_start = serializers.DateTimeField(
        help_text='Дата и время начала приема',
        label=None,
        required=False)

    class Meta:
        model = Appointment
        fields = ('id', 'datetime_start')


class AppointmentCreateSerializer(serializers.Serializer):
    """Сериализатор записи к специальности врача организации."""

    fio_pattern = re.compile(r'([А-ЯЁ][а-яё]+)\s([А-ЯЁ][а-яё]+)\s([А-ЯЁ]['
                             r'а-яё]+)$')
    phone_pattern = re.compile(r'^(\+7|7|8)?[\s\-]?\(?[489][0-9]{2}\)?[\s\-]?'
                               r'[0-9]{3}[\s\-]?[0-9]{2}[\s\-]?[0-9]{2}$')

    fio = serializers.CharField(
        min_length=8,
        max_length=255,
        required=True,
        validators=[RegexValidator(regex=fio_pattern)],
        help_text='ФИО пациента'
    )

    phone = serializers.CharField(
        required=True,
        validators=[RegexValidator(regex=phone_pattern)],
        help_text='Номер телефона пациента')

    email = serializers.EmailField(
        min_length=4,
        max_length=254,
        required=True,
        help_text='Электронная почта пациента')


class SignUpSerializer(serializers.Serializer):
    """Сериализатор регистрации нового пользователя."""

    regex_for_password = r'[a-zA-Z0-9]{8,}'
    email = serializers.EmailField(
        max_length=254,
        required=True,
    )
    # пока заглушка в виде не менее 8 букв или цифр
    password = serializers.RegexField(
        regex_for_password,
        required=True,
    )

    def validate(self, data):
        email = data.get('email')
        password = data.get('password')
        hashed_password = make_password(password)
        data['password'] = hashed_password
        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError(
                'Пользователь с такой почтой уже существует!'
            )
        return data


class TokenSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(required=True)
