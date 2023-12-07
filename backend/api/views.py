import http

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework.response import Response

from organizations.models import Organization, Specialty
from .filters import SearchFilterWithCustomDescription, SpecialtyFilter
from .mixins import (RetrieveListViewSet, NoPaginationMixin)
from .paginators import CustomNumberPagination
from .serializers import OrganizationSerializer, SpecialtySerializer
from .utils import count_distance


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
            .prefetch_related('specialties')
            .annotate(distance=count_distance(long, lat))
            .order_by('distance')
            .all()
        )

    serializer_class = OrganizationSerializer
    filter_backends = [DjangoFilterBackend, SearchFilterWithCustomDescription]
    filterset_class = SpecialtyFilter
    search_fields = ('=inn',)
    pagination_class = CustomNumberPagination
    http_method_names = ['get', 'post', 'head', 'delete', 'patch']
    lookup_field = 'uuid'


class SpecialtyViewSet(NoPaginationMixin,
                       RetrieveListViewSet):
    """Вью-сет для специальности."""

    queryset = Specialty.objects.all()
    serializer_class = SpecialtySerializer
