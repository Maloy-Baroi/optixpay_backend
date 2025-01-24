from rest_framework import serializers


def validation_error_return(message):
    return serializers.ValidationError({"status": False, "data": {}, "message": message})
