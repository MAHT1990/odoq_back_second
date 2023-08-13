from rest_framework.views import APIView
from common._RES import make_response
from . import services
from middleware.CSRF import csrf_decorator


class NoticeView(APIView):
    def get(self, request):
        # print('getnotice called')
        result = services.GetNoticesService(request).make_data()
        response = make_response(
            'success',
            'Notice is successfully fetched',
            result,
        )
        return response


class NoticeDetailView(APIView):
    def get(self, request, notice_id):
        # print('GetPostDetailService get called')
        # print('post_id is ', post_id)
        result = services.GetNoticeDetailService(request, notice_id).make_data()
        response = make_response(
            'success' if result['success'] else 'error',
            '',
            result['data'],
        )
        return response
