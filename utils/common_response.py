from rest_framework.response import Response


def CommonResponse(status_type, data=None, status_code=None):
    if status_type == "error":
        return Response({"status": False, data: data}, status=status_code)
    else:
        return Response({"status": True, data: data}, status=status_code)

