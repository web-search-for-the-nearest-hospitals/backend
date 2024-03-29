from django.utils.decorators import method_decorator
from drf_yasg.utils import swagger_auto_schema

from .mixins import NoPaginationMixin, ListViewSet
from .models import Specialty
from .schemas import SPEC_SCHEMAS
from .serializers import SpecialtySerializer


@method_decorator(
    name="list",
    decorator=swagger_auto_schema(
        tags=SPEC_SCHEMAS["list"]["tags"],
        operation_summary=SPEC_SCHEMAS["list"]["summary"],
        operation_description=SPEC_SCHEMAS["list"]["description"],
        security=[]
    )
)
class SpecialtyViewSet(NoPaginationMixin,
                       ListViewSet):
    """Вью-сет для специальности."""

    queryset = Specialty.objects.all()
    serializer_class = SpecialtySerializer
