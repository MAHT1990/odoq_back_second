from rest_framework.views import APIView
from common._RES import makeResponse
from . import services, serializers
from middleware.CSRF import csrf_decorator

class SMSView(APIView):
    @csrf_decorator
    def post(self, request):
        result = services.SendAuthorSMS(request.data)()

        return makeResponse(
            'success' if result['success'] else 'error',
            result['message'],
        )