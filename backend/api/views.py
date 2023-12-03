import http

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import action
from rest_framework.response import Response

from organizations.models import Organization, Specialty
from .filters import SearchFilterWithCustomDescription
from .mixins import RetrieveListViewSet, NoPaginationMixin
from .paginators import CustomNumberPagination
from .serializers import (OrganizationListSerializer,
                          OrganizationRetrieveSerializer,
                          SpecialtySerializer)
from .utils import count_distance


class OrganizationViewSet(RetrieveListViewSet):
    queryset = Organization.objects.all()

    serializer_class = OrganizationListSerializer
    filter_backends = [DjangoFilterBackend, SearchFilterWithCustomDescription]
    search_fields = ('=inn',)

    pagination_class = CustomNumberPagination

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return OrganizationRetrieveSerializer
        return OrganizationListSerializer

    @action(detail=False, methods=['GET'], url_path='nearest',
            filter_backends=[])
    def nearest(self, request):
        """Список организаций по удалению от координат"""

        long = request.query_params.get('long')
        lat = request.query_params.get('lat')

        if not (long and lat):
            return Response(
                status=http.HTTPStatus.BAD_REQUEST,
                data={'detail': 'Необходимо передать параметры long и lat'})

        try:
            long = float(long)
            lat = float(lat)
        except ValueError:
            return Response(
                status=http.HTTPStatus.BAD_REQUEST,
                data={'detail': 'long и lat должны быть типа float'}
            )

        orgs = (
            Organization
            .objects
            .annotate(distance=count_distance(long, lat))
            .order_by('distance')
        )
        page = self.paginate_queryset(orgs)
        serializer = self.get_serializer(page, many=True)
        if page:
            return self.get_paginated_response(serializer.data)
        return Response(serializer.data)


class SpecialtyViewSet(NoPaginationMixin,
                       RetrieveListViewSet):
    """Вью-сет для тегов."""

    queryset = Specialty.objects.all()
    serializer_class = SpecialtySerializer
