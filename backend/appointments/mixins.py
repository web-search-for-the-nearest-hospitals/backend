from rest_framework import mixins, viewsets


class UpdateViewSet(mixins.UpdateModelMixin,
                    viewsets.GenericViewSet):
    """Миксин для PUT метода."""
    pass


class NoPaginationMixin:
    """Миксин без пагинации."""

    pagination_class = None
