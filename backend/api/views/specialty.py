from django.utils.decorators import method_decorator
from drf_yasg.utils import swagger_auto_schema

from organizations.models import Specialty
from ..mixins import (NoPaginationMixin, ListViewSet)
from ..schemas import SPEC_SCHEMAS
from ..serializers import SpecialtySerializer


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
