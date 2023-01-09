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
        SmsHistoryAuth, on_delete=models.CASCADE,
        null=True
        )
    is_succeed = models.BooleanField(default=False)
    sent_at = models.DateTimeField(auto_now_add=True)

    @staticmethod
    def send_message(send_to, is_auth=False, content=''):
        '''
        문자 발송용 static method.
        - send_to : 수신자 전화번호
        - 일반 문자: is_auth = False / content = 입력받음.
        - 인증용 문자: is_auth = True / content = 생성로직을 따름.
        '''
        import requests
        #문자 발송용 API 관련
        params = {
            'key': settings.ALIGO['API_KEY'],
            'userid': settings.ALIGO['USER_ID'],
            'sender': settings.ALIGO['SENDER'],
            'receiver': str(send_to),
            'msg': content
        }

        url = "https://apis.aligo.in/send/"
        content = content
        result = False

        if(is_auth):
            import random
            code = '{0:06d}'.format(random.randrange(999999))
            content = f'인증번호 [{code}]를 입력창에 3분이내로 입력해주세요.'


        with requests.post(url, data=params) as response:
            data = response.json()
            result = data['message'] == 'success'
        
        auth = SmsHistoryAuth.objects.create(
            code=code,
            expired_at=SMS_HISTORY_AUTH_EXPIRE()
            ) if is_auth else None

        SmsHistory.objects.create(
            sms_type='SMS', 
            send_to = send_to,
            content=content,
            auth = auth, 
            is_succeed=result
        ).save()

        return result
    
    @staticmethod
    def verify_code(send_to, code):
        '''
        * 해당번호(send_to)로 보낸 마지막 SmsHistory를 찾는다.
        * 마지막 SmsHistory 기록의 auth 필드가 존재하고, 아직 인증이 완료안됐으면
          만료일시와 현재 시각을 비교하고
        * 받은 code값을 비교하여, 인증을 완료한 후 저장
        * return : 0 if 성공 else -1
        '''
        last_auth = SmsHistory.objects.filter(
            sms_type='SMS', 
            send_to=send_to
            ).order_by('-sent_at').first()
        if(last_auth):
            if (last_auth.auth.is_auth == False):
                if(last_auth.auth.expired_at > timezone.now()):
                    if(last_auth.auth.code == code.strip()):
                        last_auth.auth.is_auth = True
                        last_auth.save()
                        return 0
                    else:
                        print('인증 실패 - 코드 불일치')
                else:
                    print('인증 실패 - 인증 요청 만료시간 초과')
            else:
                print('이미 인증된 요청입니다.')
        else:
            print('인증 실패 - 인증요청내역 없음')
        return -1

class Admin(models.Model):
    email = models.EmailField()
    encrypted_password = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    phone = models.CharField(max_length=255)