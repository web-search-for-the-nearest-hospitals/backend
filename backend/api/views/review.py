from rest_framework.response import Response
from rest_framework.generics import get_object_or_404
from rest_framework.pagination import LimitOffsetPagination

from ..permissions import IsAuthorOrIsAuthenticated
from ..serializers import ReviewSerializer
from rest_framework import viewsets

from user.models import User
from organizations.models import Organization


class ReviewViewSet(viewsets.ModelViewSet):
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
