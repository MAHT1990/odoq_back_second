from rest_framework.views import APIView
from middleware.CSRF import csrf_decorator
from common._RES import make_response
from common._ENCRYPT import ENCRYPT
from common._JWT import JWT
import odoq_models.models as OdoqModels
from .login import dictionaries

USER_MODEL = OdoqModels.User


class EditUserView(APIView):
    @csrf_decorator
    def patch(self, request):
        try:
            user = USER_MODEL.get_user_by_id(request.data['userId'])
            users_by_name = USER_MODEL.get_user_by_name(request.data['userName'])
        except USER_MODEL.DoesNotExist:
            return make_response('error', '계정을 찾을 수 없습니다.')
        except Exception as e:
            return make_response('error', '닉네임 변경오류.')

        if not ENCRYPT.validate(request.data['password'], user.encrypted_password):
            return make_response('error', '비밀번호가 일치하지 않습니다.')

        if users_by_name.count() > 0:
            return make_response('error', '닉네임이 중복되었습니다.')

        user.name = request.data['userName']
        user.save()
        token = JWT.sign(user.id, user.grade, user.name)
        data = dictionaries.GetDataTable(token).make_data()
        data['userName'] = user.name
        return make_response(
            'success',
            '닉네임 수정 완료',
            data
        )
