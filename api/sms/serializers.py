from rest_framework import serializers


class SendAuthorSMS(serializers.Serializer):
  answerCount = serializers.IntegerField(required=False)
  solveCount = serializers.IntegerField(required=False)
  solveCount = serializers.FloatField(required=False)