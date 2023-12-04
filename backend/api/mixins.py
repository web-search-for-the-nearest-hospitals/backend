from rest_framework import mixins, viewsets


class RetrieveListCreateDestroyViewSet(mixins.RetrieveModelMixin,
                                       mixins.ListModelMixin,
                                       mixins.CreateModelMixin,
                                       mixins.DestroyModelMixin,
                                       viewsets.GenericViewSet):
    """Миксин для RETRIEVE, LIST, POST, DELETE методов."""
    pass


class RetrieveListViewSet(mixins.RetrieveModelMixin,
                          mixins.ListModelMixin,
                          viewsets.GenericViewSet):
    """Миксин для RETRIEVE & LIST методов."""
    pass


class NoPaginationMixin:
    """Миксин без пагинации."""

    pagination_class = None
