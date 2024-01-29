from rest_framework import viewsets
from rest_framework.generics import get_object_or_404
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.response import Response

from organizations.models import Organization
from .permissions import IsAuthorOrIsAuthenticated
from .serializers import ReviewSerializer


class ReviewViewSet(viewsets.ModelViewSet):
    """Вьюсет для отзывов."""
    serializer_class = ReviewSerializer

    permission_classes = (
        IsAuthorOrIsAuthenticated,
    )

    pagination_class = LimitOffsetPagination

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

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(
            instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)
