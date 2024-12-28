from rest_framework.response import Response


def CommonResponse(type, data=None, status_code=None):
    if type == "error":
        return Response({"status": False, data: data}, status=status_code)
    else:
        return Response({"status": True, data: data}, status=status_code)

