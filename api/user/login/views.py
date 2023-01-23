from django.http import JsonResponse
from rest_framework.views import APIView
from common._RES import makeResponse
import odoq_models.models as OdoqModels
from common._ENCRYPT import ENCRYPT
from common._JWT import JWT
from . import dictionaries
from middleware.CSRF import csrf_decorator


def index(request):
    return JsonResponse({
        'logintest': 'logintest',
    })


class LoginUserModel(APIView):
  @csrf_decorator
  def post(self, request):
    email = request.data['email']
    password = request.data['password']
    users = OdoqModels.User.objects.filter(email=email)

    if users.count() > 0:
      for user in users:
        if ENCRYPT.validate(password, user.encrypted_password):
          token = JWT.sign(user.id, 0, user.name)
          return makeResponse(
            'success',
            '',
            dictionaries.GetDataTable(token).make_data()
          )
      return makeResponse(
        'error',
        '비밀번호가 일치하지 않습니다.',
        error_code='411'
      )
    else:
      return makeResponse(
        'error',
        '계정을 찾을 수 없습니다.',
        error_code='411'
      )