from rest_framework import serializers
from rest_framework.response import Response
from django.http import JsonResponse


class ResponseClass(object):
    def __init__(self, result, message, data=dict(), error_code=''):
        self.result = result
        self.error_code = error_code
        self.message = message
        self.data = data or dict()


class ResponseSerializer(serializers.Serializer):
    result = serializers.CharField(allow_blank=True)
    error_code = serializers.CharField(allow_blank=True)
    message = serializers.CharField(allow_blank=True)
    data = serializers.DictField()

    class Meta:
        model = None


def make_response(result, message, data={}, status_code=200, error_code=''):
    response_data = ResponseClass(result, message, data, error_code)
    return Response(ResponseSerializer(response_data).data, status=status_code)


def mid_response(result, message, data={}, status_code=200, error_code=''):
    response_data = ResponseClass(result, message, data, error_code)
    return JsonResponse(ResponseSerializer(response_data).data, status=status_code)


def service_response(success: bool, data: dict):
    return {'success': success, 'data': data}


"""
사용법
from _RES import make_response

return make_response(result, message, data, status_code=200, error_code='200/400/500..')


"""
