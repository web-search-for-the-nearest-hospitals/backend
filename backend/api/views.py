import http

from django.utils.decorators import method_decorator
from django_filters.rest_framework import DjangoFilterBackend
from drf_yasg.utils import swagger_auto_schema
from rest_framework import viewsets
from rest_framework.response import Response

from organizations.models import Organization, Specialty, Town
from .filters import SearchFilterWithCustomDescription, OrgFilter
from .mixins import (RetrieveListViewSet, NoPaginationMixin)
from .paginators import CustomNumberPagination
from .serializers import (OrganizationSerializer, SpecialtySerializer,
                          TownSerializer)
from .schemas import ORGS_SCHEMAS, SPEC_SCHEMAS, TOWN_SCHEMAS
from .utils import count_distance


@method_decorator(
    name="list",
    decorator=swagger_auto_schema(
        tags=ORGS_SCHEMAS["list"]["tags"],
        operation_summary=ORGS_SCHEMAS["list"]["summary"],
        operation_description=ORGS_SCHEMAS["list"]["description"],
        pagination_class=CustomNumberPagination)
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
    LAT, LONG = 54.513675, 36.261342

    def get_queryset(self):
        """Переопределяем, чтобы сортировать результаты
        выборки по отдаленности от переданных координат."""

        long = self.request.query_params.get('long', self.LONG)
        lat = self.request.query_params.get('lat', self.LAT)

        try:
            long = float(long)
            lat = float(lat)
        except ValueError:
            return Response(
                status=http.HTTPStatus.BAD_REQUEST,
                data={'detail': 'long и lat должны быть типа float'}
            )

        return (
            Organization
            .objects
            .prefetch_related('specialties', 'district', 'town')
            .annotate(distance=count_distance(long, lat))
            .order_by('distance')
            .all()
        )

    serializer_class = OrganizationSerializer
    filter_backends = [DjangoFilterBackend, SearchFilterWithCustomDescription]
    filterset_class = OrgFilter
    search_fields = ('full_name', 'short_name')
    pagination_class = CustomNumberPagination
    http_method_names = ['get', 'post', 'head', 'delete', 'patch']
    lookup_field = 'uuid'


@method_decorator(
    name="list",
    decorator=swagger_auto_schema(
        tags=SPEC_SCHEMAS["list"]["tags"],
        operation_summary=SPEC_SCHEMAS["list"]["summary"],
        operation_description=SPEC_SCHEMAS["list"]["description"],
    )
)
@method_decorator(
    name="retrieve",
    decorator=swagger_auto_schema(
        tags=SPEC_SCHEMAS["retrieve"]["tags"],
        operation_summary=SPEC_SCHEMAS["retrieve"]["summary"],
        operation_description=SPEC_SCHEMAS["retrieve"]["description"],
        responses=SPEC_SCHEMAS["retrieve"]["responses"])
)
class SpecialtyViewSet(NoPaginationMixin,
                       RetrieveListViewSet):
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

    queryset = Town.objects.all()
    serializer_class = TownSerializer
