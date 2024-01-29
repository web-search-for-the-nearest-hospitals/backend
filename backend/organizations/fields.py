from django.shortcuts import get_object_or_404
from rest_framework import serializers


class SlugRelatedFieldWith404(serializers.SlugRelatedField):

    def to_internal_value(self, data):
        queryset = self.get_queryset()
        return get_object_or_404(queryset.filter(**{self.slug_field: data}))
