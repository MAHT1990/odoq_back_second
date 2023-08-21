from rest_framework.views import APIView
from common._RES import make_response
from . import services, serializers
from middleware.CSRF import csrf_decorator


class CommentView(APIView):
    def __get_post_or_notice(self, request):
        if request.path.find('post') != -1:
            self.post_or_notice = 'post'
        if request.path.find('notice') != -1:
            self.post_or_notice = 'notice'

    def get(self, request, id):
        # print('GetPostsService get called')
        # print('request.path', request.path)
        self.__get_post_or_notice(request)
        service_response = services.GetCommentsService(
            request, self.post_or_notice, id).make_data()
        response = make_response(
            'success' if service_response['success'] else 'fail',
            '',
            service_response['data'],
        )
        return response

    @csrf_decorator
    def post(self, request, id):
        self.__get_post_or_notice(request)
        # 대댓글 분기.
        if request.data.get('cocomment'):
            cocomment_before_validated = serializers.CocommentSerializer(data=request.data)
            if cocomment_before_validated.is_valid():
                cocomment_before_validated.save()
        else:
            comment_before_validated = serializers.CommentSerializer(data=request.data)
            if comment_before_validated.is_valid():
                comment_before_validated.save()

        service_response = services.GetCommentsService(
            request,
            self.post_or_notice,
            id
        ).make_data()

        response = make_response(
            'success' if service_response['success'] else 'fail',
            '댓글이 성공적으로 등록되었습니다.',
            service_response['data'],
        )
        return response

    @csrf_decorator
    def patch(self, request, id):
        """
        좋아요 및 댓글의 수정 및 블라인드를 담당하는 함수
        """
        # print('updateComment get called')
        # print('request.data is ', request.data)

        flag = request.data.get('flag', None)
        comment_flag = request.data.get('commentFlag', None)
        if comment_flag == 'cocomment':
            handlers = {
                'edit': services.EditCocommentService(request),
                'blind': services.BlindCocomment(request),
            }
        else:  # comment_flag == 'comment'
            handlers = {
                'edit': services.EditCommentService(request),
                'blind': services.BlindCommentService(request),
            }

        service_response = handlers[flag].make_data()

        if flag == 'like':
            if service_response['success']:
                result_message = '좋아요가 성공적으로 반영되었습니다.'
            else:
                result_message = '좋아요 반영에 실패했습니다.'

        elif flag == 'edit':
            if service_response['success']:
                result_message = '댓글이 성공적으로 수정되었습니다.'
            else:
                result_message = '댓글 수정에 실패했습니다.'

        elif flag == 'blind':
            if service_response['success']:
                if service_response['data']['blind']:
                    result_message = '댓글이 비공개 처리되었습니다.'
                else:
                    result_message = '댓글이 공개 처리되었습니다.'
            else:
                result_message = '댓글 처리에 실패했습니다.'

        return make_response(
            'success' if service_response['success'] else 'error',
            result_message,
            service_response['data'],
        )