from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination

class MyPageNumberPagination(PageNumberPagination):
    def get_paginated_response(self, data):
        return Response({
            'password_count': self.page.paginator.count,
            'next_page': self.get_next_link(),
            'previous_page': self.get_previous_link(),
            'passwords': data,
        })
