from rest_framework import mixins, viewsets


class RetrieveListViewSet(mixins.RetrieveModelMixin,
                          mixins.ListModelMixin,
                          viewsets.GenericViewSet):
    """Миксин для RETRIEVE & LIST методов."""
    pass


class UpdateViewSet(mixins.UpdateModelMixin,
                    viewsets.GenericViewSet):
    """Миксин для PATCH метода."""
    pass


class ListViewSet(mixins.ListModelMixin,
                  viewsets.GenericViewSet):
    """Миксин для LIST метода."""
    pass


class NoPaginationMixin:
    """Миксин без пагинации."""

    pagination_class = None
