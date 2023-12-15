import http

from django.utils.decorators import method_decorator
from django_filters.rest_framework import DjangoFilterBackend
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import viewsets
from rest_framework.response import Response

from organizations.models import Organization, Specialty, Town
from .filters import SearchFilterWithCustomDescription, OrgFilter
from .mixins import (RetrieveListViewSet, NoPaginationMixin)
from .paginators import CustomNumberPagination
from .serializers import (OrganizationSerializer, SpecialtySerializer,
                          TownSerializer)
from .utils import count_distance


@method_decorator(
    name="list",
    decorator=swagger_auto_schema(
        tags=['Организации'],
        operation_summary="Список организаций",
        operation_description=("Страница доступна всем пользователям. "
                               "Доступен поиск по ИНН."),
        pagination_class=CustomNumberPagination)
)
@method_decorator(
    name="retrieve",
    decorator=swagger_auto_schema(
        tags=['Организации'],
        operation_summary="Получение организации",
        operation_description="Страница доступна всем пользователям.",
        responses={
            '404': openapi.Response('Страница не найдена.',
                                    examples={
                                        "application/json": {
                                            "detail": "Страница не найдена."}
                                    })
        }
    ),
)
@method_decorator(
    name="create",
    decorator=swagger_auto_schema(
        tags=['Организации'],
        operation_summary="Добавление организации",
        operation_description="Страница доступна всем пользователям.",
    ),
)
@method_decorator(
    name="destroy",
    decorator=swagger_auto_schema(
        tags=['Организации'],
        operation_summary="Удаление организации",
        operation_description="Страница доступна всем пользователям.",
    ),
)
@method_decorator(
    name="partial_update",
    decorator=swagger_auto_schema(
        tags=['Организации'],
        operation_summary="Обновление организации",
        operation_description="Страница доступна всем пользователям.",
    ),
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
    search_fields = ('=inn',)
    pagination_class = CustomNumberPagination
    http_method_names = ['get', 'post', 'head', 'delete', 'patch']
    lookup_field = 'uuid'


@method_decorator(
    name="list",
    decorator=swagger_auto_schema(
        tags=['Специальности врачей'],
        operation_summary="Список специальностей",
        operation_description=("Страница доступна всем пользователям."),
    )
)
class SpecialtyViewSet(NoPaginationMixin,
                       RetrieveListViewSet):
    """Вью-сет для специальности."""

    queryset = Specialty.objects.all()
    serializer_class = SpecialtySerializer


class TownViewSet(NoPaginationMixin,
                  RetrieveListViewSet):
    """Вью-сет для города."""

    queryset = Town.objects.all()
    serializer_class = TownSerializer
