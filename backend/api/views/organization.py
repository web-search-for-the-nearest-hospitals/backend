import http

from django.utils.decorators import method_decorator
from django_filters.rest_framework import DjangoFilterBackend
from drf_yasg.utils import swagger_auto_schema
from rest_framework import viewsets, permissions, decorators, response

from organizations.models import Appointment, Organization
from ..filters import SearchFilterWithCustomDescription, OrgFilter
from ..mixins import NoPaginationMixin
from ..paginators import CustomNumberPagination
from ..schemas import ORGS_SCHEMAS
from ..serializers import (AppointmentListSerializer,
                           OrganizationCreateUpdateSerializer,
                           OrganizationListSerializer,
                           OrganizationRetrieveSerializer,
                           AppointmentParamSerializer)


@method_decorator(
    name="list",
    decorator=swagger_auto_schema(
        tags=ORGS_SCHEMAS["list"]["tags"],
        operation_summary=ORGS_SCHEMAS["list"]["summary"],
        operation_description=ORGS_SCHEMAS["list"]["description"],
        pagination_class=CustomNumberPagination,
        manual_parameters=ORGS_SCHEMAS["list"]["params"])
)
@method_decorator(
    name="retrieve",
    decorator=swagger_auto_schema(
        tags=ORGS_SCHEMAS["retrieve"]["tags"],
        operation_summary=ORGS_SCHEMAS["retrieve"]["summary"],
        operation_description=ORGS_SCHEMAS["retrieve"]["description"],
        responses=ORGS_SCHEMAS["retrieve"]["responses"])
)
@method_decorator(
    name="create",
    decorator=swagger_auto_schema(
        tags=ORGS_SCHEMAS["create"]["tags"],
        operation_summary=ORGS_SCHEMAS["create"]["summary"],
        operation_description=ORGS_SCHEMAS["create"]["description"])
)
@method_decorator(
    name="destroy",
    decorator=swagger_auto_schema(
        tags=ORGS_SCHEMAS["destroy"]["tags"],
        operation_summary=ORGS_SCHEMAS["destroy"]["summary"],
        operation_description=ORGS_SCHEMAS["destroy"]["description"])
)
@method_decorator(
    name="partial_update",
    decorator=swagger_auto_schema(
        tags=ORGS_SCHEMAS["partial_update"]["tags"],
        operation_summary=ORGS_SCHEMAS["partial_update"]["summary"],
        operation_description=ORGS_SCHEMAS["partial_update"]["description"])
)
class OrganizationViewSet(viewsets.ModelViewSet):
    """Вью-сет организации."""

    ACTIONS_WITH_ONE_INSTANCE = ('retrieve', 'delete', 'partial_update',
                                 'get_free_tickets')

    def get_queryset(self):
        """Оптимизируем походы в базу данных."""

        if self.action in self.ACTIONS_WITH_ONE_INSTANCE:
            return (
                Organization
                .objects
                .prefetch_related('specialties', 'business_hours')
                .all()
            )
        return (
            Organization
            .objects
            .prefetch_related('business_hours')
            .select_related('town', 'district')
            .all()
        )

    def filter_queryset(self, queryset):
        """Убираем фильтрацию с действий, работающих с одной сущностью."""

        if self.action in self.ACTIONS_WITH_ONE_INSTANCE:
            return queryset
        return super().filter_queryset(queryset)

    def get_serializer_class(self):
        """Определяем какой сериализатор использовать в зависимости от
        метода."""

        if self.action == 'retrieve':
            return OrganizationRetrieveSerializer
        if self.action == 'list':
            return OrganizationListSerializer
        return OrganizationCreateUpdateSerializer

    def get_permissions(self):
        """Временная заглушка, чтобы не баловались POST-методами."""

        if self.action in ('create', 'update', 'destroy'):
            permission_classes = [permissions.IsAuthenticated]
        else:
            permission_classes = [permissions.AllowAny]
        return [permission() for permission in permission_classes]

    filter_backends = [DjangoFilterBackend, SearchFilterWithCustomDescription]
    filterset_class = OrgFilter
    search_fields = ('short_name',)
    pagination_class = CustomNumberPagination
    # http_method_names = ['get', 'post', 'head', 'delete', 'patch']
    http_method_names = ['get', 'head']
    lookup_field = 'uuid'

    @swagger_auto_schema(
        name="get_free_tickets",
        tags=ORGS_SCHEMAS["get_free_tickets"]["tags"],
        operation_summary=ORGS_SCHEMAS["get_free_tickets"]["summary"],
        operation_description=ORGS_SCHEMAS["get_free_tickets"]["description"],
        pagination_class=NoPaginationMixin,
        responses={"200": AppointmentListSerializer},
        query_serializer=AppointmentParamSerializer,
    )
    @decorators.action(detail=True,
                       methods=['GET'],
                       url_path='free-tickets',
                       url_name='org-free-tickets',
                       filter_backends=[])
    def get_free_tickets(self, request, uuid):
        """Формирует свободные диапазоны времени для
        переданных даты и специальности врача."""

        serializer = AppointmentParamSerializer(data=request.query_params)
        serializer.is_valid(raise_exception=True)

        which_date = serializer.validated_data.get('which_date')
        spec = serializer.validated_data.get('spec_code')

        free_appointments = (
            Appointment
            .objects
            .only('id', 'datetime_start')
            .filter(organization__uuid=uuid, status='free', specialty=spec,
                    datetime_start__date=which_date)
            .all()
        )
        serializer = AppointmentListSerializer(free_appointments, many=True)
        return response.Response(status=http.HTTPStatus.OK,
                                 data=serializer.data)