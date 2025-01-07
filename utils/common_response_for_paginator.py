from rest_framework.response import Response
from rest_framework import status


def CommonResponseForPaginator(status_type, data_with_others=None, status_code=status.HTTP_200_OK, message=None):
    # Ensure data_with_others is a dictionary if none is provided
    if data_with_others is None:
        data_with_others = {}

    # Extract data and remove 'data' key safely
    data = data_with_others.pop('data', None)

    response_body = {
        "status": status_type == "success",
        "data": data if data is not None else {},
        "message": message
    }

    # Merge additional pagination data if available
    response_body.update(data_with_others)

    return Response(response_body, status=status_code)
