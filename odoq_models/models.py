from django.db import models

# Create your models here.
from django.db import models
from django.utils import timezone

# Create your models here.
class User(models.Model):
    email = models.EmailField(unique=True)
    encrypted_password = models.CharField(max_length=255, null=True)
    name = models.CharField(max_length=255)
    phone = models.CharField(max_length=255)

def SMS_HISTORY_AUTH_EXPIRE():
    return timezone.now() + timezone.timedelta(minutes=3)

class SmsHistoryAuth(models.Model):
    code = models.CharField(max_length=255)
    is_auth = models.BooleanField(default=False)
    expired_at = models.DateTimeField(default=SMS_HISTORY_AUTH_EXPIRE())

class SmsHistory(models.Model):
    sms_type = models.CharField(max_length=255)
    send_to = models.CharField(max_length=255)
    content = models.CharField(max_length=255)
    auth = models.OneToOneField(SmsHistoryAuth, on_delete =models.CASCADE)
    is_succeed = models.BooleanField(default=False)
    sent_at = models.DateTimeField(auto_now_add=True)

    @staticmethod
    def send_message(send_to, is_auth=False, content=''):
        import urllib.parse, urllib.request
        import xmltodict
        import json

        content = content
        code = ''

        if(is_auth):
            import random
            code = '{0:06d}'.format(random.randrage(999999))
            content = f'인증번호 [{code}]를 입력창에 3분이내로 입력해주세요.'

        params = {
            'key': 'dtwkui1b8e5yux73rl5e5c3g666yt861',
            'user_id': 'aloe89',
            'sender': '01077650903',
            'receiver': '01092445161',
            'msg': 'text문자발송.'
        }

        url = "https://apis.aligo.in/send/" + urllib.parse.urlencode(params)

        result = False
        with urllib.request.urlopen(url) as response:
            data = xmltodict.parse(response.read())
            result = (data['result_code']==1)
            print(result)