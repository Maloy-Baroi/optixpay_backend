from rest_framework import status
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

from utils.common_response import CommonResponse


class CustomPagination(PageNumberPagination):
    page_size = 10  # Default number of items per page
    page_size_query_param = 'page_size'  # Allow client to override, e.g., ?page_size=20
    max_page_size = 100  # Maximum limit allowed when requested by client

    def get_paginated_response(self, data):
        return CommonResponse("success", {
            'next': self.get_next_link(),
            'previous': self.get_previous_link(),
            'current_page': self.page.number,
            'total_pages': self.page.paginator.num_pages,
            'results_per_page': self.page.paginator.per_page,
            'total_results': self.page.paginator.count,
            'results': data
        }, status.HTTP_200_OK if len(data) > 0 else status.HTTP_400_BAD_REQUEST, "Data Found!" if len(data) > 0 else "Data Not Found!")
