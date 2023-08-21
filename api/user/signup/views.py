from rest_framework.views import APIView
from common._RES import make_response
from . import services
from middleware.CSRF import csrf_decorator

class RegistUser(APIView):
  @csrf_decorator
  def post(self, request):
    result = services.RegistUser(request.data)()

    return make_response(
      'success' if result['success'] else 'error',
      result['message'],
      result.get('data', None)
    )

class SendSMSAuthView(APIView):
  @csrf_decorator
  def post(self, request):
    result = services.SendSMSAuthService(request.data)()

    return make_response(
      'success' if result['success'] else 'error',
      result['message'],
    )


class VerifySMSAuth(APIView):
  @csrf_decorator
  def post(self, request):
    result = services.VerifySMSAuth(request.data)()

    return make_response(
      'success' if result['success'] else 'error',
      result['message'],
    )