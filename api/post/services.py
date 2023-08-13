import odoq_models.models as OdoqModels
import datetime
from math import ceil
from django.core.paginator import Paginator
from django.db.models import Q


USER_MODEL = OdoqModels.User
POST_MODEL = OdoqModels.Post
COMMENT_MODEL = OdoqModels.Comment
COCOMMENT_MODEL = OdoqModels.Cocomment


class GetPostsService:

    def __init__(self, request):
        # print('request.GET in post.services is ', request.GET)
        # print('request.data in post.services is ', request.data)
        self.request = request
        self.page_number = int(request.GET.get('pageNumber', 1))
        self.page_size = int(request.GET.get('pageSize', 15))

        # get으로 넘어올 수도 있고, post로 넘어올 수도 있다.
        self.filtering_flag = request.GET.get(
            'filteringFlag',
            request.data.get('filteringFlag', 'all')
        )
        self.ordering_flag = request.GET.get(
            'orderingFlag',
            request.data.get('orderingFlag', 'latest')
        )
        self.user_id = request.GET.get(
            'userId',
            request.data.get('user', '')
        )

    def _get_comments_count(self, post):
        comments_count = COMMENT_MODEL.get_comments_by_post(post.id).count()
        cocomments_count = 0
        for comment in post.comments.all():
            cocomments_count += COCOMMENT_MODEL.get_cocomments_by_comment(comment.id).count()
        return comments_count + cocomments_count

    def _get_list_posts(self):
        limit, offset = self.page_size * self.page_number, self.page_size * (self.page_number - 1)

        if self.filtering_flag == 'all':
            queryset_post = POST_MODEL.get_all_type_posts()
            queryset_post_page = queryset_post[offset:limit]
            self.total_posts = queryset_post.count()

        if self.filtering_flag == 'solution':
            queryset_post = POST_MODEL.get_solution_type_posts()
            queryset_post_page = queryset_post[offset:limit]
            self.total_posts = queryset_post.count()

        if self.filtering_flag == 'my':
            queryset_post = POST_MODEL.get_post_by_id(self.user_id)
            queryset_post_page = queryset_post[offset:limit]
            self.total_posts = queryset_post.count()

        # ordering
        if self.ordering_flag == 'likeCount':
            queryset_post_page = queryset_post_page.order_by('-like_count', '-created_at')
            self.total_posts = queryset_post_page.count()

        list_temp_posts = []
        for post in queryset_post_page:
            list_temp_posts.append({
                'id': post.id,
                'type': post.type,
                'user_id': post.user.id,
                'user_grade': post.user.grade,
                'user_level': post.user.get_user_level(),
                'user_name': post.user.name,
                'title': post.title,
                # 'content': post.content,
                'img_url': post.img.url if post.img else None,
                'hit_count': post.hit_count,
                'like_count': post.like_count,
                'liked_users': [user.id for user in post.liked_users.all()],
                'created_at': post.created_at,
                # 'updated_at': post.updated_at,
                'blind': post.blind,
                'blind_text': post.blind_text,
                'comments_count': self._get_comments_count(post),
            })
        self.posts = list_temp_posts
        self.total_pages = ceil(self.total_posts / self.page_size)

    def make_data(self):
        self._get_list_posts()
        data = {
            'posts': self.posts,
            'total_posts': self.total_posts,
            'today_posts': len(list(filter(
                lambda x: (x['created_at'] + datetime.timedelta(hours=9)).date() == datetime.date.today(), self.posts
                )
            )),
            'current_page': 1,
            'total_pages': 1,
        }
        try:
            data['current_page'] = self.page_number
            data['total_pages'] = self.total_pages
            # print(self.data)
        except Exception as e:
            pass
        # print(data)
        return data


class GetPostDetailService:
    def __init__(self, request, post_id):
        self.post_id = post_id

    def _get_post(self):
        if self.post_id is None:
            return
        try:
            self.post = POST_MODEL.get_post_by_id(self.post_id)
            if self.post is None:
                return
            self.__hit_count()
        except Exception as e:
            return

    def __hit_count(self):
        self.post.hit_count += 1
        self.post.save()

    def make_data(self):
        self._get_post()
        data = {
            'post': {
                'id': self.post.id,
                'user_id': self.post.user.id,
                'user_grade': self.post.user.grade,
                'user_level': self.post.user.get_user_level(),
                'user_name': self.post.user.name,
                'title': self.post.title,
                'type': self.post.type,
                'content': self.post.content,
                'img_url': self.post.img.url if self.post.img else None,
                'hit_count': self.post.hit_count,
                'like_count': self.post.like_count,
                'liked_users': [user.id for user in self.post.liked_users.all()],
                'created_at': self.post.created_at,
                'updated_at': self.post.updated_at,
                'blind': self.post.blind,
                'blind_text': self.post.blind_text,
            }
        } if self.post else None
        # print(data)
        return {
            'success': True if data else False,
            'data': data,
        }


class LikePostService:
    def __init__(self, request):
        # print('request.data in LikePostService is ', request.data)
        self.post_id = request.data.get('postId', None)
        self.user_id = request.data.get('userId', None)

        self.post = POST_MODEL.get_post_by_id(self.post_id)
        self.user = USER_MODEL.get_user_by_id(self.user_id)

    def _like_post(self):
        if self.post is None or self.user is None:
            self.data = {
                'success': False,
            }
            return

        if self.post in self.user.like_posts.all():  # 좋아요 취소
            self.user.like_posts.remove(self.post)
            self.post.like_count -= 1
        else:  # 좋아요
            self.user.like_posts.add(self.post)
            self.post.like_count += 1

        self.post.save()
        self.data = {
            'success': True,
            'like_count': self.post.like_count,
            'user_id': self.user_id,
            'post_id': self.post_id,
        }

    def make_data(self):
        self._like_post()
        return self.data


class BlindPostService:
    def __init__(self, request):
        self.post_id = request.data.get('postId', None)
        self.user_grade = request.data.get('userGrade', None)

    def _blind_post(self):
        # print('post/services.py > BlindPostService self.user_grade is ', self.user_grade, type(self.user_grade))
        if self.post_id is None:
            self.data = {
                'success': False,
            }
            return

        post = POST_MODEL.get_post_by_id(self.post_id)
        post.blind = not post.blind
        post.blind_text = '관리자에 의해 블라인드 처리되었습니다.' if self.user_grade == 2 else post.blind_text
        post.save()
        self.data = {
            'success': True,
            'blind': post.blind,
            'blind_text': post.blind_text,
            'post_id': self.post_id,
        }
        # print('post/services.py > BlindPostService self.data is ', self.data)

    def make_data(self):
        self._blind_post()
        return self.data

class DeletePostService:
    def __init__(self, request, post_id):
        self.post_id = post_id

    def _delete_post(self):
        try:
            if self.post_id is None:
                raise Exception('post_id is None')
            post = POST_MODEL.get_post_by_id(self.post_id)
            post.delete()
            self.data = {
                'success': True,
                'post_id': self.post_id,
            }
        except Exception as e:
            self.data = {
                'success': False,
            }
            return

    def make_data(self):
        self._delete_post()
        return self.data