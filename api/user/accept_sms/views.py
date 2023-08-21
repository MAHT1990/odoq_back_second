from rest_framework.views import APIView
from common._RES import make_response
from middleware.CSRF import csrf_decorator
from . import services

class AcceptSMSView(APIView):
    def get(self, request):
        result = services.GetAcceptSMSService(request).make_data()
        response = make_response(
            'success',
            'SMS 수신여부를 성공적으로 조회하였습니다.',
            result,
        )
        return response
    @csrf_decorator
    def patch(self, request):
        result = services.CheckAcceptSMSService(request).make_data()
        response = make_response(
            'success',
            'SMS 수신여부가 성공적으로 반영되었습니다.',
            result,
        )
        return response