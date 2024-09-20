from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination

class MyPageNumberPagination(PageNumberPagination):
    page_size = 6  # Display 6 items per page
    page_size_query_param = 'page_size'
    max_page_size = 10  # Optional limit for maximum page size
    def get_paginated_response(self, data):
        return Response({
            'password_items_count' : self.page.paginator.count,
            'next_page' : self.get_next_link(),
            'previous_page' : self.get_previous_link(),
            'passwords' : data,
        })