from rest_framework import serializers


class RegistUser(serializers.Serializer):
  email = serializers.CharField(required=True)
  password = serializers.CharField(required=True)
  name = serializers.CharField(required=True)
  phone = serializers.CharField(required=True)
  advertising_consent = serializers.BooleanField(required=True)

  class Meta:
    model = None

class SendSMSAuth(serializers.Serializer):
  phone = serializers.CharField(required=True)

  class Meta:
    model = None


class VerifySMSAuth(serializers.Serializer):
  phone = serializers.CharField(required=True)
  code = serializers.CharField(required=True)

  class Meta:
    mode = None