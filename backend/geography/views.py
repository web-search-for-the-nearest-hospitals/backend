import http

from django.shortcuts import get_object_or_404
from django.utils.decorators import method_decorator
from drf_yasg.utils import swagger_auto_schema
from rest_framework import decorators, response

from specialties.serializers import SpecialtySerializer
from specialties.models import Specialty
from .mixins import RetrieveListViewSet, NoPaginationMixin
from .models import Town
from .schemas import TOWN_SCHEMAS
from .serializers import TownRetrieveSerializer, TownListSerializer


@method_decorator(
    name="list",
    decorator=swagger_auto_schema(
        tags=TOWN_SCHEMAS["list"]["tags"],
        operation_summary=TOWN_SCHEMAS["list"]["summary"],
        operation_description=TOWN_SCHEMAS["list"]["description"],
        security=[]
    )
)
@method_decorator(
    name="retrieve",
    decorator=swagger_auto_schema(
        tags=TOWN_SCHEMAS["retrieve"]["tags"],
        operation_summary=TOWN_SCHEMAS["retrieve"]["summary"],
        operation_description=TOWN_SCHEMAS["retrieve"]["description"],
        responses=TOWN_SCHEMAS["retrieve"]["responses"],
        manual_parameters=TOWN_SCHEMAS["retrieve"]["params"],
        security=[])
)
class TownViewSet(NoPaginationMixin,
                  RetrieveListViewSet):
    """Вью-сет для города."""
    lookup_value_regex = r'\d+'

    def get_queryset(self):
        """Оптимизируем походы в базу данных."""

        if self.action == 'retrieve':
            return Town.objects.prefetch_related('districts').all()
        if self.action == 'list':
            return Town.objects.only('id', 'name').all()
        return Town.objects.all()

    def get_serializer_class(self):
        """Определяем какой сериализатор использовать в зависимости от
        метода."""

        if self.action == 'retrieve':
            return TownRetrieveSerializer
        return TownListSerializer

    @swagger_auto_schema(
        name="get_free_tickets",
        tags=TOWN_SCHEMAS["get_specialties"]["tags"],
        operation_summary=TOWN_SCHEMAS["get_specialties"]["summary"],
        operation_description=TOWN_SCHEMAS["get_specialties"]["description"],
        pagination_class=NoPaginationMixin,
        responses={"200": SpecialtySerializer(many=True),
                   "404": TOWN_SCHEMAS["get_specialties"]["responses"]},
        manual_parameters=TOWN_SCHEMAS["get_specialties"]["params"],
        security=[]
    )
    @decorators.action(detail=True,
                       methods=['GET'],
                       url_path='specialties',
                       url_name='town-specialties',
                       filter_backends=[])
    def get_specialties(self, request, pk):
        """Формирует список имеющихся специальностей врачей в городе,
         <id> которого передан."""

        town = get_object_or_404(Town.objects.only('id'), pk=pk)

        specialties = (
            Specialty
            .objects
            .only('code', 'skill', 'name')
            .filter(organizations__organization__town_id=town.pk)
            .distinct('skill')
        )
        serializer = SpecialtySerializer(specialties, many=True)
        return response.Response(status=http.HTTPStatus.OK,
                                 data=serializer.data)
