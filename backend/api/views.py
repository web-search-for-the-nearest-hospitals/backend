from django.utils.decorators import method_decorator
from django_filters.rest_framework import DjangoFilterBackend
from drf_yasg.utils import swagger_auto_schema
from rest_framework import viewsets, permissions

from organizations.models import Appointment, Organization, Specialty, Town
from .filters import SearchFilterWithCustomDescription, OrgFilter
from .mixins import (RetrieveListViewSet, NoPaginationMixin, ListViewSet)
from .paginators import CustomNumberPagination
from .schemas import ORGS_SCHEMAS, SPEC_SCHEMAS, TOWN_SCHEMAS
from .serializers import (OrganizationCreateUpdateSerializer,
                          OrganizationListSerializer,
                          OrganizationRetrieveSerializer, SpecialtySerializer,
                          TownSerializer)


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

    def get_queryset(self):
        """Оптимизируем походы в базу данных."""

        if self.action in ('retrieve', 'delete', 'partial_update'):
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


@method_decorator(
    name="list",
    decorator=swagger_auto_schema(
        tags=SPEC_SCHEMAS["list"]["tags"],
        operation_summary=SPEC_SCHEMAS["list"]["summary"],
        operation_description=SPEC_SCHEMAS["list"]["description"],
    )
)
class SpecialtyViewSet(NoPaginationMixin,
                       ListViewSet):
    """Вью-сет для специальности."""

    queryset = Specialty.objects.all()
    serializer_class = SpecialtySerializer


@method_decorator(
    name="list",
    decorator=swagger_auto_schema(
        tags=TOWN_SCHEMAS["list"]["tags"],
        operation_summary=TOWN_SCHEMAS["list"]["summary"],
        operation_description=TOWN_SCHEMAS["list"]["description"],
    )
)
@method_decorator(
    name="retrieve",
    decorator=swagger_auto_schema(
        tags=TOWN_SCHEMAS["retrieve"]["tags"],
        operation_summary=TOWN_SCHEMAS["retrieve"]["summary"],
        operation_description=TOWN_SCHEMAS["retrieve"]["description"],
        responses=TOWN_SCHEMAS["retrieve"]["responses"])
)
class TownViewSet(NoPaginationMixin,
                  RetrieveListViewSet):
    """Вью-сет для города."""

    queryset = Town.objects.prefetch_related('districts').all()
    serializer_class = TownSerializer
