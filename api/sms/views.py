from rest_framework.views import APIView
from common._RES import makeResponse
from . import services, serializers
from middleware.CSRF import csrf_decorator

class SMSView(APIView):
    @csrf_decorator
    def post(self, request):
        if (request.data['target'] == 'author'):
            result = services.SendAuthorSMS(request.data)()
        if (request.data['target'] == 'student'):
            result = services.SendStudentSMS(request.data)()

        return makeResponse(
            'success' if result['success'] else 'error',
            result['message'],
        )