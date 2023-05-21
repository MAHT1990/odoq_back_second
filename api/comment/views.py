from rest_framework.views import APIView
from common._RES import makeResponse
from . import services, serializers
from middleware.CSRF import csrf_decorator

class CommentView(APIView):
    def __get_post_or_notice(self, request):
        if request.path.find('post') != -1:
            self.post_or_notice = 'post'
        if request.path.find('notice') != -1:
            self.post_or_notice = 'notice'


    def get(self, request, id):
        # print('GetPosts get called')
        # print('request.path', request.path)
        self.__get_post_or_notice(request)
        result = services.GetComments(
            request,
            self.post_or_notice,
            id).make_data()
        response = makeResponse(
            'success',
            '',
            result,
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

        result = services.GetComments(
            request,
            self.post_or_notice,
            id
        ).make_data()

        # print('result is ', result);

        response = makeResponse(
            'success',
            '댓글이 성공적으로 등록되었습니다.',
            result,
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
                'edit': services.EditCocomment(request),
                'blind': services.BlindCocomment(request),
            }
        else:  # comment_flag == 'comment'
            handlers = {
                'edit': services.EditComment(request),
                'blind': services.BlindComment(request),
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