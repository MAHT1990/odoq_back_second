from utils import common
import odoq_models.models as OdoqModels
from django.db import Error, IntegrityError, transaction

from common._ENCRYPT import ENCRYPT
from common._JWT import JWT

from . import serializers


class RegistUser():
    def __init__(self, request_data):
        self.request_data = serializers.RegistUser(data=request_data)

    def __call__(self):
        if self.request_data.is_valid():
            if self.__is_duplicate_email():
                return {'success': False, 'message': '이미 가입되어있는 이메일 입니다.'}

            if self.__is_duplicate_phone():
                return {'success': False, 'message': '이미 가입되어있는 연락처 입니다.'}

            try:
                with transaction.atomic():
                    encrypted_password = ENCRYPT.encrypt(self.request_data.data['password'])
                    user = OdoqModels.User(
                        email=self.request_data.data['email'],
                        encrypted_password=encrypted_password,
                        name=self.request_data.data['name'],
                        grade = 0,
                        phone=self.request_data.data['phone'],
                    )
                    user.save()

                if not user:
                    return {'success': True, 'message': '오류가 발생했습니다. 다시 시도해주세요'}

                # 로그인
                token = JWT.sign(user.id, user.grade, user.name)

                return {'success': True, 'message': None, 'data': {'token': token}}
            except IntegrityError as e:
                # print(e)
                return {'success': False, 'message': e.message}
            except Error as e:
                # print(e)
                return {'success': False, 'message': e.message}

        else:
            # print('serializers에서 잘못되었음')
            return {'success': False, 'message': common.serializer_error_message(self.request_data.errors)}

    def __is_duplicate_email(self):
        email = self.request_data.data['email']
        user = OdoqModels.User.objects.filter(email=email).first()
        if user is not None:
            return True

        super_admin = OdoqModels.Admin.objects.filter(email=email).first()
        if super_admin is not None:
            return True

        return False

    def __is_duplicate_phone(self):
        phone = self.request_data.data['phone']
        user = OdoqModels.User.objects.filter(phone=phone).first()
        if user is not None:
            return True
        return False

class SendSMSAuth():
    def __init__(self, request_data):
        self.request_data = serializers.SendSMSAuth(data=request_data)

    def __call__(self):
        if self.request_data.is_valid():
            target_phone = self.request_data.data['phone']

            result = OdoqModels.SmsHistory.send_message(send_to=target_phone, is_auth=True)

            if result:
                return {'success': True, 'message': None}
            else:
                return {'success': False, 'message': '인증번호 발송요청에 실패하였습니다.'}
        else:
            return {'success': False, 'message': common.serializer_error_message(self.request_data.errors)}


class VerifySMSAuth():
    def __init__(self, request_data):
        self.request_data = serializers.VerifySMSAuth(data=request_data)

    def __call__(self):
        '''
        관련 serializer로 validation 이후,
        전화번호(target_phone)와 code를 받아
        Model : SmsHistory의 인증 로직으로 전달 -> return : 0 or -1
        인증 로직의 결과에 따라 dict 만들어 return.
        '''
        if self.request_data.is_valid():
            target_phone = self.request_data.data['phone']
            code = self.request_data.data['code']

            result = OdoqModels.SmsHistory.verify_code(send_to=target_phone, code=code)

            if result == 0:
                return {'success': True, 'message': None}
            else:
                return {'success': False, 'message': '인증에 실패하였습니다.'}
        else:
            return {'success': False, 'message': common.serializer_error_message(self.request_data.errors)}
