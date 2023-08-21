from rest_framework.views import APIView
from common._RES import make_response
from . import services
from middleware.CSRF import csrf_decorator


class NoticeView(APIView):
    def get(self, request):
        # print('getnotice called')
        service_response = services.GetNoticesService(request).make_data()
        response = make_response(
            'success' if service_response['success'] else 'fail',
            'Notice is successfully fetched',
            service_response['data'],
        )
        return response


class NoticeDetailView(APIView):
    def get(self, request, notice_id):
        # print('GetPostDetailService get called')
        # print('post_id is ', post_id)
        service_response = services.GetNoticeDetailService(request, notice_id).make_data()
        response = make_response(
            'success' if service_response['success'] else 'error',
            '',
            service_response['data'],
        )
        return response
