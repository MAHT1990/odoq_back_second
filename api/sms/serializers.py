from rest_framework import serializers


class SendAuthorSMS(serializers.Serializer):
  answerCount = serializers.IntegerField(required=False)
  solveCount = serializers.IntegerField(required=False)
  solveCount = serializers.FloatField(required=False)
  target = serializers.CharField(required=False)

class SendStudentSMS(serializers.Serializer):
  content = serializers.CharField(required=False)
  url = serializers.CharField(required=False)
  target = serializers.CharField(required=False)