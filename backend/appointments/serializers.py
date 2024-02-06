import datetime

from django.core.validators import RegexValidator
from rest_framework import serializers

from .models import Appointment
from .utils import FIO_REGEX, PHONE_NUMBER_REGEX


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

    fio = serializers.CharField(
        min_length=8,
        max_length=255,
        required=True,
        validators=[RegexValidator(regex=FIO_REGEX)],
        help_text='ФИО пациента'
    )

    phone = serializers.CharField(
        required=True,
        validators=[RegexValidator(regex=PHONE_NUMBER_REGEX)],
        help_text='Номер телефона пациента')
