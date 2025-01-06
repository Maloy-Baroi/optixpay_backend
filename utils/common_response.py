from rest_framework.response import Response
from rest_framework import status


def CommonResponse(status_type, data=None, status=None, message=None):
    """
    Generates a common format for API responses.

    Args:
    - status_type (str): "success" or "error" indicating the response type.
    - data (dict, optional): Data to be included in the response.
    - status (int, optional): HTTP status code to be returned with the response.

    Returns:
    - Response: DRF Response object with specified data and status.
    """
    if status_type == "error":
        return Response({"status": False, "data": data, "message": message}, status=status)
    else:
        return Response({"status": True, "data": data, "message": message}, status=status)
