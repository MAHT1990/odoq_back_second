import datetime
from math import ceil
from django.core.paginator import Paginator
import odoq_models.models as OdoqModels
from common._RES import service_response


COMMENT_MODEL = OdoqModels.Comment
COCOMMENT_MODEL = OdoqModels.Cocomment


class GetCommentsService:
    def __init__(self, request, flag, post_id):
        self.flag = flag
        self.post_id = post_id
        self.page_size = 100
        self.page_number = request.GET.get('page', 1)

    def _get_list_comments(self):
        list_temp_comments = []
        if self.flag == 'post':
            comments_queryset = COMMENT_MODEL.get_comments_by_post(self.post_id)
        if self.flag == 'notice':
            comments_queryset = COMMENT_MODEL.get_comments_by_notice(self.post_id)
        for comment in comments_queryset:
            list_temp_comments.append({
                'id': comment.id,
                'user_id': comment.user.id,
                'user_grade': comment.user.grade,
                'user_level': comment.user.get_user_level(),
                'user_name': comment.user.name,
                'content': comment.content,
                'created_at': comment.created_at,
                'updated_at': comment.updated_at,
                'blind': comment.blind,
                'blind_text': comment.blind_text,
                'cocomments': [{
                    'id': cocomment.id,
                    'user_id': cocomment.user.id,
                    'user_grade': cocomment.user.grade,
                    'user_level': cocomment.user.get_user_level(),
                    'user_name': cocomment.user.name,
                    'content': cocomment.content,
                    'created_at': cocomment.created_at,
                    'updated_at': cocomment.updated_at,
                    'blind': cocomment.blind,
                    'blind_text': cocomment.blind_text,
                    } for cocomment in comment.cocomments.all()
                ],
            })
        self.comments = list_temp_comments

    def make_data(self):
        self._get_list_comments()
        data = {}
        try:
            pagination = Paginator(self.comments, self.page_size)
            list_result_comments = pagination.page(self.page_number).object_list
            data['comments'] = list_result_comments
            data['current_page'] = pagination.page(self.page_number).number
            data['total_pages'] = pagination.num_pages
            data['total_comments'] = pagination.count
            success = True

        except Exception as e:
            data['comments'] = []
            data['current_page'] = 1
            data['total_pages'] = 1
            data['total_comments'] = 0
            success = False
        return service_response(success, data)


class EditCommentService:
    def __init__(self, request):
        self.target_id = request.data.get('targetId', None)
        self.content = request.data.get('content', None)
        self.data = {}
        self.success = None;

    def _set_target_model(self):
        self.target_model = COMMENT_MODEL

    def _edit_target(self):
        if self.target_id is None:
            self.success = False
            return

        target = self.target_model.objects.get(id=self.target_id)
        target.content = self.content
        target.save()

        self.success = True
        self.data = {
            'target_id': self.target_id,
            'content': self.content,
        }

    def make_data(self):
        self._set_target_model()
        self._edit_target()
        return service_response(self.success, self.data)


class BlindCommentService:
    def __init__(self, request):
        self.target_id = request.data.get('targetId', None)
        self.user_grade = request.data.get('userGrade', None)
        self.success = None
        self.data = {}

    def _set_target_model(self):
        self.target_model = COMMENT_MODEL

    def _blind_comment(self):
        # print('post/services.py > BlindPostService self.user_grade is ', self.user_grade, type(self.user_grade))
        if self.target_id is None:
            self.success = False
            return

        target = self.target_model.objects.get(id=self.target_id)
        target.blind = not target.blind
        target.blind_text = '관리자에 의해 블라인드 처리되었습니다.' if self.user_grade == 2 else target.blind_text
        target.save()
        self.success = True
        self.data = {
            'blind': target.blind,
            'blind_text': target.blind_text,
            'target_id': self.target_id,
        }
        # print('post/services.py > BlindPostService self.data is ', self.data)

    def make_data(self):
        self._set_target_model()
        self._blind_comment()
        return service_response(self.success, self.data)


class EditCocommentService(EditCommentService):
    def _set_target_model(self):
        self.target_model = COCOMMENT_MODEL


class BlindCocomment(BlindCommentService):
    def _set_target_model(self):
        self.target_model = COCOMMENT_MODEL
