import odoq_models.models as OdoqModels
import datetime
from math import ceil
from django.core.paginator import Paginator

class GetComments:
    def __init__(self, request, flag, post_id):
        self.flag = flag
        self.post_id = post_id
        self.data = {}
        self.page_size = 100
        self.page_number = request.GET.get('page', 1)

    def _get_list_comments(self):
        list_temp_comments = []
        if self.flag == 'post':
            comments_queryset = OdoqModels.Comment.objects.filter(post_id=self.post_id)
        if self.flag == 'notice':
            comments_queryset = OdoqModels.Comment.objects.filter(notice_id=self.post_id)
        for comment in comments_queryset:
            list_temp_comments.append({
                'id': comment.id,
                'user_id': comment.user.id,
                'user_grade': comment.user.grade,
                'user_level': comment.user.solved_questions.count(),
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
                    'user_level': cocomment.user.solved_questions.count(),
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
        try:
            pagination = Paginator(self.comments, self.page_size)
            list_result_comments = pagination.page(self.page_number).object_list
            self.data['comments'] = list_result_comments
            self.data['current_page'] = pagination.page(self.page_number).number
            self.data['total_pages'] = pagination.num_pages
            self.data['total_comments'] = pagination.count

        except Exception as e:
            self.data['comments'] = []
            self.data['current_page'] = 1
            self.data['total_pages'] = 1
            self.data['total_comments'] = 0
            self.data['today_comments'] = 0
        return self.data


class EditComment:
    def __init__(self, request):
        self.target_id = request.data.get('targetId', None)
        self.content = request.data.get('content', None)

    def _set_target_model(self):
        self.target_model = OdoqModels.Comment

    def _edit_target(self):
        if self.target_id is not None:
            target = self.target_model.objects.get(id=self.target_id)
            target.content = self.content
            target.save()
            self.data = {
                'success': True,
                'target_id': self.target_id,
                'content': self.content,
            }
        else:
            self.data = {
                'success': False,
            }

    def make_data(self):
        self._set_target_model()
        self._edit_target()
        return self.data


class BlindComment:
    def __init__(self, request):
        self.target_id = request.data.get('targetId', None)
        self.user_grade = request.data.get('userGrade', None)

    def _set_target_model(self):
        self.target_model = OdoqModels.Comment

    def _blind_comment(self):
        # print('post/services.py > BlindPost self.user_grade is ', self.user_grade, type(self.user_grade))
        if self.target_id is not None:
            target = self.target_model.objects.get(id=self.target_id)
            target.blind = not target.blind
            target.blind_text = '관리자에 의해 블라인드 처리되었습니다.' if self.user_grade == 2 else target.blind_text
            target.save()
            self.data = {
                'success': True,
                'blind': target.blind,
                'blind_text': target.blind_text,
                'target_id': self.target_id,
            }
            # print('post/services.py > BlindPost self.data is ', self.data)
        else:
            self.data = {
                'success': False,
            }

    def make_data(self):
        self._set_target_model()
        self._blind_comment()
        return self.data


class EditCocomment(EditComment):
    def _set_target_model(self):
        self.target_model = OdoqModels.Cocomment


class BlindCocomment(BlindComment):
    def _set_target_model(self):
        self.target_model = OdoqModels.Cocomment