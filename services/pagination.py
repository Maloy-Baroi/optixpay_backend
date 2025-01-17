from traceback import print_tb

from rest_framework import status
from rest_framework.pagination import PageNumberPagination
from utils.common_response import CommonResponse
from utils.common_response_for_paginator import CommonResponseForPaginator


class CustomPagination(PageNumberPagination):
    page_size = 10  # Default number of items per page
    page_size_query_param = 'page_size'  # Allow client to override, e.g., ?page_size=20
    max_page_size = 100  # Maximum limit allowed when requested by client

    def get_paginated_response(self, data):
        if len(data) > 0:
            status_type = "success"
            message = "Data Found!"
            http_status = status.HTTP_200_OK
        else:
            status_type = "error"
            message = "Data Not Found!"
            http_status = status.HTTP_204_NO_CONTENT

        return CommonResponseForPaginator(status_type, {
            'next': self.get_next_link(),
            'previous': self.get_previous_link(),
            'current_page': self.page.number,
            'total_pages': self.page.paginator.num_pages,
            'results_per_page': self.page.paginator.per_page,
            'total_results': self.page.paginator.count,
            'data': data
        }, http_status, message)
