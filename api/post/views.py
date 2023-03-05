from rest_framework.views import APIView
from common._RES import makeResponse
import odoq_models.models as OdoqModels
from . import services, serializers

class PostView(APIView):
    def get(self, request):
        # print('getPost get called')
        result = services.GetPost(request).make_data()
        response = makeResponse(
            'success',
            '',
            result,
        )
        return response

    def post(self, request):
        # print('createPost get called')
        # print('request.data is ', request.data)
        post_before_validated = serializers.PostSerializer(data=request.data)
        if post_before_validated.is_valid():
            post_before_validated.save()
            result = services.GetPost(request).make_data()

        # print('result is ', result);

        response = makeResponse(
            'success',
            '댓글이 성공적으로 등록되었습니다.',
            result,
        )
        return response


    def patch(self, request):
        '''
        좋아요 및 게시글의 수정을 담당하는 함수
        '''
        # print('updatePost get called')
        # print('request.data is ', request.data)

        flag = request.data.get('flag', None)
        if flag == 'like':
            result = services.LikePost(request).make_data()
            # print('result of like functionality is ', result)
            if result['success']:
                result_message = '좋아요가 성공적으로 반영되었습니다.'
            else:
                result_message = '좋아요 반영에 실패했습니다.'

        elif flag == 'update':
            pass

        response = makeResponse(
            'success',
            result_message,
            result,
        )
        return response