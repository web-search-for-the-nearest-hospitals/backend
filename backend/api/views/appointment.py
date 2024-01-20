import http

from django.db import transaction
from django.shortcuts import get_object_or_404
from django.utils.decorators import method_decorator
from drf_yasg.utils import swagger_auto_schema
from rest_framework import response

from organizations.models import Appointment
from user.models import User
from ..mixins import NoPaginationMixin, UpdateViewSet
from ..schemas import APPOINT_SCHEMAS
from ..serializers import AppointmentCreateSerializer


@method_decorator(
    name="update",
    decorator=swagger_auto_schema(
        tags=APPOINT_SCHEMAS["update"]["tags"],
        operation_summary=APPOINT_SCHEMAS["update"]["summary"],
        operation_description=APPOINT_SCHEMAS["update"]["description"],
        responses=APPOINT_SCHEMAS["update"]["responses"],
        security=[])
)
class AppointmentViewSet(NoPaginationMixin,
                         UpdateViewSet):
    """Вью-сет для записи к врачу."""

    queryset = Appointment.objects.all()
    serializer_class = AppointmentCreateSerializer
    http_method_names = ['put']

    def update(self, request, *args, **kwargs):
        """
        Изменяем свойства талона записи к врачу - добавляем пользователя
        к нему.
        SELECT ... FOR UPDATE используется для устранения race condition.
        Во втором релизе отсюда уйдет перезапись свойств
        пользователя и его создание.
        """
        serializer = self.get_serializer(
            data=request.data,
            partial=kwargs.pop('partial', False))

        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        last_name, first_name, third_name = data.pop('fio').split()

        with transaction.atomic():
            instance = get_object_or_404(
                Appointment
                .objects
                .only('id', 'status')
                .select_for_update(), pk=kwargs.get('pk')
            )
            if instance.status != Appointment.FREE:
                return response.Response(
                    status=http.HTTPStatus.BAD_REQUEST,
                    data={"detail": "Этот талон уже занят"})

            # Создание пользователя здесь - это следствие неуспеваемости
            # фронта в реализации регистрации пользователей

            user, _ = (
                User
                .objects
                .only('id')
                .get_or_create(email=data.get('email'))
            )
            user.last_name = last_name
            user.first_name = first_name
            user.third_name = third_name
            user.phone = data.get('phone')
            user.save(
                update_fields=['last_name', 'first_name',
                               'third_name', 'phone']
            )

            instance.client, instance.status = user, Appointment.PLANNED
            instance.save(update_fields=['client', 'status'])

        return response.Response(status=http.HTTPStatus.NO_CONTENT)
