from rest_framework.views import APIView
from common._RES import makeResponse
from . import services

class NoticeView(APIView):
    def get(self, request):
        # print('getnotice called')
        result = services.GetNotice(request).make_data()
        response = makeResponse(
            'success',
            'Notice is successfully fetched',
            result,
        )
        return response