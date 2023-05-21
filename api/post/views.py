from rest_framework.views import APIView
from common._RES import makeResponse
from . import services, serializers
from middleware.CSRF import csrf_decorator
from api.comment.views import CommentView


class PostView(APIView):
    def get(self, request):
        # print('GetPosts get called')
        result = services.GetPosts(request).make_data()
        response = makeResponse(
            'success',
            '',
            result,
        )
        return response

    @csrf_decorator
    def post(self, request):
        # print('createPost get called')
        # print('request.data is ', request.data)
        post_before_validated = serializers.PostSerializer(data=request.data)
        if post_before_validated.is_valid():
            post_before_validated.save()
            result = services.GetPosts(request).make_data()

        # print('result is ', result);

        response = makeResponse(
            'success',
            '댓글이 성공적으로 등록되었습니다.',
            result,
        )
        return response

    @csrf_decorator
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

        elif flag == 'blind':
            result = services.BlindPost(request).make_data()
            # print('result of blind functionality is ', result)
            if result['success']:
                if result['blind']:
                    result_message = '게시글이 비공개 처리되었습니다.'
                else:
                    result_message = '게시글이 공개 처리되었습니다.'
            else:
                result_message = '게시글 처리에 실패했습니다.'

        response = makeResponse(
            'success',
            result_message,
            result,
        )
        return response


class PostDetailView(APIView):
    def get(self, request, post_id):
        # print('getPostDetail get called')
        # print('post_id is ', post_id)
        result = services.GetPostDetail(request, post_id).make_data()
        response = makeResponse(
            'success' if result['success'] else 'error',
            '',
            result['data'],
        )
        return response

    def delete(self, request, post_id):
        # print('deletePost get called')
        result = services.DeletePost(request, post_id).make_data()
        # print('result of delete functionality is ', result)
        if result['success']:
            result_message = '게시글이 성공적으로 삭제되었습니다.'
        else:
            result_message = '게시글 삭제에 실패했습니다.'

        response = makeResponse(
            'success' if result['success'] else 'error',
            result_message,
            result,
        )
        return response