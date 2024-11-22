from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from django.conf import settings

from urllib.parse import urlparse, urlunparse

class MyPageNumberPagination(PageNumberPagination):
    page_size = 6  # Display 6 items per page
    page_size_query_param = 'page_size'
    max_page_size = 10  # Optional limit for maximum page size

    def get_next_link(self):
        link = super().get_next_link()
        if link:
            parsed_url = urlparse(link)
            # if parsed_url.scheme == 'http':
            #     link = urlunparse(parsed_url._replace(scheme='https'))
            if getattr(settings, 'CORS_ALLOWED_ORIGINS', []) == ["http://localhost:3000"]:
                link = urlunparse(parsed_url._replace(scheme='https'))
        return link

    def get_previous_link(self):
        link = super().get_previous_link()
        if link:
            parsed_url = urlparse(link)
            # if parsed_url.scheme == 'http':
            #     link = urlunparse(parsed_url._replace(scheme='https'))
            if getattr(settings, 'CORS_ALLOWED_ORIGINS', []) == ["http://localhost:3000"]:
                link = urlunparse(parsed_url._replace(scheme='https'))
        return link

    def get_paginated_response(self, data):
        return Response({
            'password_items_count': self.page.paginator.count,
            'next_page': self.get_next_link(),
            'previous_page': self.get_previous_link(),
            'passwords': data,
        })
