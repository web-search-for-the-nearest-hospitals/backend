from rest_framework import mixins, viewsets


class RetrieveListViewSet(mixins.RetrieveModelMixin,
                          mixins.ListModelMixin,
                          viewsets.GenericViewSet):
    """Миксин для RETRIEVE & LIST методов."""
    pass


class NoPaginationMixin:
    """Миксин без пагинации."""

    pagination_class = None
