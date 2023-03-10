from utils import common
import odoq_models.models as OdoqModels
from . import serializers

class SendAuthorSMS():
    def __init__(self, request_data):
        self.request_data = serializers.SendAuthorSMS(data=request_data)

    def __call__(self):
        if self.request_data.is_valid():
            # target_phone = self.request_data.data['phone']
            target_phone_query_set = OdoqModels.User.objects.filter(grade=1)
            target_phone_list = [user.phone for user in target_phone_query_set]
            print('target_phone_list in SendAuthorSMS Service: ', target_phone_list)
            content = f"제출 답안수는 {self.request_data.data['answerCount']} 입니다."
            print(content)

            for target_phone in target_phone_list:
                result = OdoqModels.SmsHistory.send_message(send_to=target_phone, is_auth=False, content=content)
                print(result)
            # result = OdoqModels.SmsHistory.send_message(send_to=target_phone, is_auth=False, content=content)

            # if result:
            #     return {'success': True, 'message': None}
            # else:
            #     return {'success': False, 'message': '문자 발송요청에 실패하였습니다.'}
            return {'success': True, 'message': None}
        else:
            return {'success': False, 'message': common.serializer_error_message(self.request_data.errors)}

class SendStudentSMS():
    def __init__(self, request_data):
        self.request_data = serializers.SendStudentSMS(data=request_data)
    def __call__(self):
        if self.request_data.is_valid():
            # target_phone = self.request_data.data['phone']
            target_phone_query_set = OdoqModels.User.objects.filter(grade=0)
            target_phone_list = [user.phone for user in target_phone_query_set]
            print('target_phone_list in SendStudentSMS Service: ', target_phone_list)
            content = f"{self.request_data.data['content']}, {self.request_data.data['url']}"
            print('content in SendStudentSMS Service to student: ', content)

            for target_phone in target_phone_list:
                result = OdoqModels.SmsHistory.send_message(send_to=target_phone, is_auth=False, content=content)
                print(result)
            # result = OdoqModels.SmsHistory.send_message(send_to=target_phone, is_auth=False, content=content)

            # if result:
            #     return {'success': True, 'message': None}
            # else:
            #     return {'success': False, 'message': '문자 발송요청에 실패하였습니다.'}
            return {'success': True, 'message': None}
        else:
            return {'success': False, 'message': common.serializer_error_message(self.request_data.errors)}