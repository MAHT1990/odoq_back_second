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

def makeResponse(result, message, data={}, status_code=200, error_code=''):
  responseData = ResponseClass(result, message, data, error_code)
  return Response(ResponseSerializer(responseData).data, status=status_code)

def midResponse(result, message, data={}, status_code=200, error_code=''):
  responseData = ResponseClass(result, message, data, error_code)
  return JsonResponse(ResponseSerializer(responseData).data, status=status_code)


"""
사용법
from _RES import makeResponse

return makeResponse(result, message, data, status_code=200, error_code='200/400/500..')


"""
