from rest_framework.views import APIView
from common._RES import makeResponse
from . import services


class GetQuestion(APIView):
    def get(self, request):
        # print('getquestion called')
        result = services.GetQuestion(request).make_data()
        response = makeResponse(
            'status',
            'message',
            result,
        )
        return response