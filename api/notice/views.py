from rest_framework.views import APIView
from common._RES import makeResponse
from . import services
from middleware.CSRF import csrf_decorator


class NoticeView(APIView):
    def get(self, request):
        # print('getnotice called')
        result = services.GetNotices(request).make_data()
        response = makeResponse(
            'success',
            'Notice is successfully fetched',
            result,
        )
        return response


class NoticeDetailView(APIView):
    def get(self, request, notice_id):
        # print('GetPostDetailService get called')
        # print('post_id is ', post_id)
        result = services.GetNoticeDetail(request, notice_id).make_data()
        response = makeResponse(
            'success' if result['success'] else 'error',
            '',
            result['data'],
        )
        return response


class CommentView(APIView):
    def get(self, request, post_id):
        # print('GetPostsService get called')
        result = services.GetCommentsService(request, post_id).make_data()
        response = makeResponse(
            'success',
            '',
            result,
        )
        return response
    @csrf_decorator
    def post(self, request, post_id):
        # 대댓글 분기.
        if request.data.get('cocomment'):
            cocomment_before_validated = serializers.CocommentSerializer(data=request.data)
            if cocomment_before_validated.is_valid():
                cocomment_before_validated.save()
        else:
            comment_before_validated = serializers.CommentSerializer(data=request.data)
            if comment_before_validated.is_valid():
                comment_before_validated.save()

        result = services.GetCommentsService(request, post_id).make_data()

        # print('result is ', result);

        response = makeResponse(
            'success',
            '댓글이 성공적으로 등록되었습니다.',
            result,
        )
        return response

    @csrf_decorator
    def patch(self, request, post_id):
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

        result = handlers[flag].make_data()

        if flag == 'like':
            if result['success']:
                result_message = '좋아요가 성공적으로 반영되었습니다.'
            else:
                result_message = '좋아요 반영에 실패했습니다.'

        elif flag == 'edit':
            if result['success']:
                result_message = '댓글이 성공적으로 수정되었습니다.'
            else:
                result_message = '댓글 수정에 실패했습니다.'

        elif flag == 'blind':
            if result['success']:
                if result['blind']:
                    result_message = '댓글이 비공개 처리되었습니다.'
                else:
                    result_message = '댓글이 공개 처리되었습니다.'
            else:
                result_message = '댓글 처리에 실패했습니다.'

        return makeResponse(
            'success' if result['success'] else 'error',
            result_message,
            result,
        )