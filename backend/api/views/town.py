from django.utils.decorators import method_decorator
from drf_yasg.utils import swagger_auto_schema

from organizations.models import Town
from ..mixins import RetrieveListViewSet, NoPaginationMixin
from ..schemas import TOWN_SCHEMAS
from ..serializers import TownSerializer


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
