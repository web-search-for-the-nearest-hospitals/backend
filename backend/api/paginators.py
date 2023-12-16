from django.conf import settings
from django.utils.translation import gettext_lazy as _
from rest_framework import pagination
from rest_framework.response import Response


class CustomNumberPagination(pagination.PageNumberPagination):
    page_query_description = _('Номер страницы')
    page_size = None

    def get_page_size(self, request):
        page_size = super().get_page_size(request)
        if page_size is None:
            return settings.REST_FRAMEWORK['PAGE_SIZE']
        return page_size

    def get_paginated_response(self, data):
        return Response({
            'count': self.page.paginator.count,
            'next': self.get_next_link(),
            'previous': self.get_previous_link(),
            'results': data,
        })

    def get_paginated_response_schema(self, schema):
        return {
            'type': 'object',
            'required': '',
            'properties': {
                'count': {
                    'type': 'integer',
                    'example': 322,
                    'description': 'Общее количество объектов',
                },
                'next': {
                    'type': 'string',
                    'nullable': True,
                    'format': 'uri',
                    'description': 'Ссылка на следующую страницу'
                },
                'previous': {
                    'type': 'string',
                    'nullable': True,
                    'format': 'uri',
                    'description': 'Ссылка на предыдущую страницу'
                },
                'results': schema,
            },
        }
