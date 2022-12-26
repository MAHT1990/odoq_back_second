from django.conf import settings
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
    expired_at = models.DateTimeField()

class SmsHistory(models.Model):
    sms_type = models.CharField(max_length=255)
    send_to = models.CharField(max_length=255)
    content = models.CharField(max_length=255)
    auth = models.OneToOneField(
        SmsHistoryAuth, on_delete =models.CASCADE,
        null=True
        )
    is_succeed = models.BooleanField(default=False)
    sent_at = models.DateTimeField(auto_now_add=True)

    @staticmethod
    def send_message(send_to, is_auth=False, content=''):
        # import urllib.parse, urllib.request
        import requests
        import json

        content = content
        code = ''

        if(is_auth):
            import random
            code = '{0:06d}'.format(random.randrange(999999))
            content = f'인증번호 [{code}]를 입력창에 3분이내로 입력해주세요.'

        params = {
            'key': settings.ALIGO['API_KEY'],
            'userid': settings.ALIGO['USER_ID'],
            'sender': settings.ALIGO['SENDER'],
            'receiver': str(send_to),
            'msg': content
        }

        url = "https://apis.aligo.in/send/"

        result = False
        with requests.post(url, data=params) as response:
            data = response.json()
            result = data['message'] == 'success'
        
        auth = SmsHistoryAuth.objects.create(
            code=code,
            expired_at=SMS_HISTORY_AUTH_EXPIRE()
            ) if is_auth else None
        print(auth)
        print(auth.code)
        print(auth.expired_at)
        SmsHistory.objects.create(
            sms_type='SMS', 
            send_to = send_to,
            content=content,
            auth = auth, 
            is_succeed=result
        ).save()

        return result
    
    def verify_code(send_to, code):
        last_auth = SmsHistory.objects.filter(
            sms_type='SMS', 
            send_to=send_to
            ).order_by('-sent_at').first()
        print(last_auth)
        print(last_auth)
        if(last_auth and last_auth.auth.is_auth == False):
            # print('now is', timezone.now())
            # print('now tzinfo is', timezone.now().tzinfo)
   
            # print('last_auth.auth.expired_at is ', last_auth.auth.expired_at)
            # print('last_auth.auth.expired_at is ', last_auth.auth.expired_at.tzinfo)
                        
            if(last_auth.auth.expired_at > timezone.now()):
                if(last_auth.auth.code == code.strip()):
                    last_auth.auth.is_auth = True
                    last_auth.save()
                    return 0
                else:
                    print('인증 실패 - 코드 불일치')
            print('인증 실패 - 인증 요청 만료시간 초과')
        else:
            print('인증 실패 - 인증요청내역 없음 혹은 이미 성공한 요청')
        return -1