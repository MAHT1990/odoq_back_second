from rest_framework.views import APIView
from common._RES import makeResponse
from . import services

def index(request):
    return JsonResponse({
        'test': 'test',
    })

class GetPost(APIView):
    def get(self, request):
        print('getPost get called')
        result = services.GetPost(request).make_data()
        response = makeResponse(
            'status',
            'message',
            result,
        )
        return response