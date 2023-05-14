from django.conf import settings
from django.db import models
from django.utils import timezone


# Create your models here.
class User(models.Model):
    email = models.EmailField(unique=True)
    encrypted_password = models.CharField(max_length=255, null=True)
    name = models.CharField(max_length=255)
    grade = models.IntegerField(default=0)
    phone = models.CharField(max_length=255)
    like_posts = models.ManyToManyField('Post', blank=True, default=None, related_name='liked_users')
    # liked_cocomments = models.ManyToManyField('Cocomment', blank=True, default=None)
    answered_questions = models.ManyToManyField('Question', blank=True, default=None, related_name='answered_users')
    solved_questions = models.ManyToManyField('Question', blank=True, default=None, related_name='solved_users')
    accept_sms = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)


# SMS 인증 관련.
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
        """
        문자 발송용 static method.
        - send_to : 수신자 전화번호
        - 일반 문자: is_auth = False / content = 입력받음.
        - 인증용 문자: is_auth = True / content = 생성로직을 따름.
        """
        import requests
        # 문자 발송용 API 관련

        url = "https://apis.aligo.in/send/"
        content = content
        result = False

        if is_auth:
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
        """
        * 해당번호(send_to)로 보낸 마지막 SmsHistory를 찾는다.
        * 마지막 SmsHistory 기록의 auth 필드가 존재하고, 아직 인증이 완료안됐으면
          만료일시와 현재 시각을 비교하고
        * 받은 code값을 비교하여, 인증을 완료한 후 저장
        * return : 0 if 성공 else -1
        """
        last_auth = SmsHistory.objects.filter(
            sms_type='SMS', 
            send_to=send_to
            ).order_by('-sent_at').first()
        if last_auth:
            if not last_auth.auth.is_auth:
                if last_auth.auth.expired_at > timezone.now():
                    if last_auth.auth.code == code.strip():
                        last_auth.auth.is_auth = True
                        last_auth.save()
                        return 0
                    else:
                        # print('인증 실패 - 코드 불일치')
                        pass
                else:
                    # print('인증 실패 - 인증 요청 만료시간 초과')
                    pass
            else:
                # print('이미 인증된 요청입니다.')
                pass
        else:
            # print('인증 실패 - 인증요청내역 없음')
            pass
        return -1


class Notice(models.Model):
    title = models.CharField(max_length=255)
    img = models.ImageField(null=True)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)

    def __str__(self):
        return self.text

    class Meta:
        ordering = ["-created_at"]


class Question(models.Model):
    code = models.CharField(max_length=255)
    season = models.CharField(max_length=255)
    img = models.ImageField()
    answer = models.CharField(max_length=255)
    upload_datetime = models.DateTimeField(null = True)

    answer_count = models.PositiveIntegerField(default=0)
    solve_count = models.PositiveIntegerField(default=0)

    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)

    def __str__(self):
        return self.code


class AnswerHistory(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    answer = models.CharField(max_length=255)
    isSolved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.answer


class Post(models.Model):
    # Question과 Comment는 1 : n 의 관계이다.
    type = models.CharField(max_length=255, default='normal')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255, default='제목 만들어지기전 포스트들입니다.')
    content = models.TextField()
    img = models.ImageField(null=True)
    hit_count = models.PositiveIntegerField(default=0)
    like_count = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    blind = models.BooleanField(default=False)
    blind_text = models.CharField(
        max_length=100,
        default="작성자에 의하여 블라인드 처리되었습니다.",
        )

    class Meta:
        ordering = ['-created_at']

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    img = models.ImageField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    blind = models.BooleanField(default=False)
    blind_text = models.CharField(
        max_length=100,
        default="작성자에 의하여 블라인드 처리되었습니다.",
        )

    class Meta:
        ordering = ['created_at']


class Cocomment(models.Model):
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, related_name='cocomments')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    blind = models.BooleanField(default=False)
    blind_text = models.CharField(
        max_length=100,
        default="작성자에 의하여 블라인드 처리되었습니다.",
        )

    class Meta:
        ordering = ['created_at']


class Solution(Post):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    answer = models.CharField(max_length=255)
    isSolved = models.BooleanField(default=False)


class Admin(models.Model):
    email = models.EmailField()
    encrypted_password = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    phone = models.CharField(max_length=255)