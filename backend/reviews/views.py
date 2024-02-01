from django.utils.decorators import method_decorator
from drf_yasg.utils import swagger_auto_schema
from rest_framework import viewsets
from rest_framework.generics import get_object_or_404
from rest_framework.mixins import CreateModelMixin, ListModelMixin

from organizations.models import Organization
from organizations.paginators import CustomNumberPagination
from .permissions import IsAuthorOrIsAuthenticated
from .schemas import REVIEWS_SCHEMAS
from .serializers import ReviewSerializer, ReviewListSerializer


@method_decorator(
    name="list",
    decorator=swagger_auto_schema(
        tags=REVIEWS_SCHEMAS["list"]["tags"],
        operation_summary=REVIEWS_SCHEMAS["list"]["summary"],
        operation_description=REVIEWS_SCHEMAS["list"]["description"],
        responses=REVIEWS_SCHEMAS["list"]["responses"],
        security=[],
        manual_parameters=REVIEWS_SCHEMAS['list']['params'],
    ),
)
@method_decorator(
    name="create",
    decorator=swagger_auto_schema(
        tags=REVIEWS_SCHEMAS["create"]["tags"],
        operation_summary=REVIEWS_SCHEMAS["create"]["summary"],
        operation_description=REVIEWS_SCHEMAS["create"]["description"],
        responses=REVIEWS_SCHEMAS["create"]["responses"],
    ),
)
class ReviewViewSet(CreateModelMixin,
                    ListModelMixin,
                    viewsets.GenericViewSet):
    """Вьюсет для отзывов."""

    permission_classes = (
        IsAuthorOrIsAuthenticated,
    )

    pagination_class = CustomNumberPagination

    def get_organization(self):
        return get_object_or_404(
            Organization,
            uuid=self.kwargs.get('uuid')
        )

    def get_queryset(self):
        return self.get_organization().reviews.all()

    def perform_create(self, serializer):
        serializer.save(
            author=self.request.user, organization=self.get_organization()
        )

    def get_serializer_class(self):
        if self.action == 'list':
            return ReviewListSerializer
        return ReviewSerializer
