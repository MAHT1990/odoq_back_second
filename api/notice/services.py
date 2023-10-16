import odoq_models.models as OdoqModels
from math import ceil
from common._RES import service_response


NOTICE_MODEL = OdoqModels.Notice
COMMENT_MODEL = OdoqModels.Comment


class GetNoticesService:
    def __init__(self, request):
        self.request = request
        self.page_number = int(request.GET.get('pageNumber', 1))
        self.page_size = int(request.GET.get('pageSize', 15))

    def _get_comments_count(self, notice):
        """
        댓글 개수를 가져오는 함수
        :param notice: NOTICE_MODEL
        :return: int
        """
        comments_count = COMMENT_MODEL.get_comments_by_notice(notice.id).count()
        cocomments_count = 0
        for comment in notice.comments.all():
            cocomments_count += comment.cocomments.count()
        return comments_count + cocomments_count

    def _get_list_notices(self):
        """
        공지사항 리스트를 가져오는 함수
        :return: QuerySet
        """
        limit, offset = self.page_size * self.page_number, self.page_size * (self.page_number - 1)
        queryset_notice = NOTICE_MODEL.objects.all().order_by('-created_at')[offset:limit]
        list_temp_notices = []
        for notice in queryset_notice:
            list_temp_notices.append({
                'id': notice.id,
                'user_id': notice.user.id,
                'user_grade': notice.user.grade,
                'user_level': notice.user.get_user_level(),
                'user_name': notice.user.name,
                'title': notice.title,
                'img_url': notice.img.url if notice.img else None,
                'hit_count': notice.hit_count,
                'like_count': notice.like_count,
                'liked_users': [user.id for user in notice.liked_users.all()],
                'content': notice.content,
                'created_at': notice.created_at,
                'updated_at': notice.updated_at,
                'comments_count': self._get_comments_count(notice),
                'is_display': notice.is_display,
            })
        self.notices = list_temp_notices
        self.total_pages = ceil(NOTICE_MODEL.objects.count() / self.page_size)

    def make_data(self):
        """
        공지사항 리스트를 만드는 함수
        :return: dict
        """
        self._get_list_notices()
        return service_response(
            True,
            {
                'notices': self.notices,
                'current_page': self.page_number,
                'total_pages': self.total_pages,
            }
        )

class GetNoticeDetailService:
    def __init__(self, request, notice_id):
        self.request = request
        self.notice_id = notice_id
        self.data = {}

    def _get_notice(self):
        """
        공지사항을 가져오는 함수
        :return: NOTICE_MODEL
        """
        if self.notice_id is not None:
            try:
                self.notice = NOTICE_MODEL.objects.get(id=self.notice_id)
            except NOTICE_MODEL.DoesNotExist:
                self.notice = None
        if self.notice is not None:
            self.__hit_count()

    def __hit_count(self):
        """
        조회수를 늘리는 함수
        :return: None
        """
        self.notice.hit_count += 1
        self.notice.save()

    def make_data(self):
        """
        공지사항을 만드는 함수
        :return: dict
        """
        self._get_notice()
        if self.notice is not None:
            self.data = {
                'notice': {
                    'id': self.notice.id,
                    'user_id': self.notice.user.id,
                    'user_grade': self.notice.user.grade,
                    'user_level': self.notice.user.get_user_level(),
                    'user_name': self.notice.user.name,
                    'title': self.notice.title,
                    'content': self.notice.content,
                    'img_url': self.notice.img.url if self.notice.img else None,
                    'file_name': self.notice.file.name if self.notice.file else None,
                    'hit_count': self.notice.hit_count,
                    'like_count': self.notice.like_count,
                    'liked_users': [user.id for user in self.notice.liked_users.all()],
                    'created_at': self.notice.created_at,
                    'updated_at': self.notice.updated_at,
                }
            }
            # print('#GetNoticeDetailService', self.data)
        return service_response(
            True if self.data else False,
            self.data
        )
