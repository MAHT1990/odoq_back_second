import odoq_models.models as OdoqModels
import datetime
from django.core.paginator import Paginator


class GetPosts:
    def __init__(self, request):
        # print('request.GET in post.services is ', request.GET)
        self.request = request
        self.page_number = request.GET.get('pageNumber', 1)
        self.page_size = request.GET.get('pageSize', 7)
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

        # print('self.ordering_flag is ', self.ordering_flag, type(self.ordering_flag))
        # print('self.filtering_flag is ', self.filtering_flag, type(self.filtering_flag))
        # print('self.filtering_flag is ', self.filtering_flag, type(self.filtering_flag))
        # print('self.user_id is ', self.user_id, type(self.user_id))
        self.data = {}

    def _get_list_posts(self):
        '''
        게시글을 가져오는 함수
        filtering_flag에 따라서 '전체' 또는 '나의' 게시글을 가져온다.
        '''
        # filtering
        queryset_post = OdoqModels.Post.objects.all()

        if self.filtering_flag == 'my':
            queryset_post = queryset_post.filter(user_id=self.user_id)

        # ordering
        if self.ordering_flag == 'likeCount':
            queryset_post = queryset_post.order_by('-like_count', '-created_at')
        list_temp_posts = []
        for post in queryset_post:
            list_temp_posts.append({
                'id': post.id,
                'user_id': post.user.id,
                'user_grade': post.user.grade,
                'user_level': post.user.solved_questions.count(),
                'user_name': post.user.name,
                'title': post.title,
                'content': post.content,
                'img_url': post.img.url if post.img else None,
                'hit_count': post.hit_count,
                'like_count': post.like_count,
                'liked_users': [user.id for user in post.liked_users.all()],
                'created_at': post.created_at,
                'updated_at': post.updated_at,
                'blind': post.blind,
                'blind_text': post.blind_text,
            })
        self.posts = list_temp_posts

    def make_data(self):
        self._get_list_posts()
        try:
            pagination = Paginator(self.posts, self.page_size)
            list_result_posts = pagination.page(self.page_number).object_list
            self.data['posts'] = list_result_posts
            self.data['current_page'] = pagination.page(self.page_number).number
            self.data['total_pages'] = pagination.num_pages
            self.data['total_posts'] = pagination.count
            self.data['today_posts'] = len(list(filter(
                lambda x: (x['created_at'] + datetime.timedelta(hours=9)).date() == datetime.date.today(), self.posts
                )
            ))

        except :
            # TODO: 아마도 today_posts에서 예외처리가 필요할 수도.
            # print('EmptyPage')
            pass
        # print(self.data)
        return self.data


class GetPostDetail:
    def __init__(self, request, post_id):
        self.post_id = post_id
        self.data = {}

    def _get_post(self):
        if self.post_id is not None:
            self.post = OdoqModels.Post.objects.get(id=self.post_id)
            self.__hit_count()

    def __hit_count(self):
        self.post.hit_count += 1
        self.post.save()

    def make_data(self):
        self._get_post()
        self.data = {
            'post': {
                'id': self.post.id,
                'user_id': self.post.user.id,
                'user_grade': self.post.user.grade,
                'user_level': self.post.user.solved_questions.count(),
                'user_name': self.post.user.name,
                'title': self.post.title,
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
        # print(self.data)
        return self.data


class LikePost:
    def __init__(self, request):
        # print('request.data in likePost is ', request.data)
        self.post_id = request.data.get('postId', None)
        self.user_id = request.data.get('userId', None)
        # print('post/services.py > LikePost self.post_id is ', self.post_id, type(self.post_id))
        # print('post/services.py > LikePost self.user_id is ', self.user_id, type(self.user_id))

    def _like_post(self):
        if self.post_id is not None and self.user_id is not None:
            user, post = OdoqModels.User.objects.get(id=self.user_id), OdoqModels.Post.objects.get(id=self.post_id)
            # print('like_posts is ', user.like_posts.all())

            if post in user.like_posts.all():
                # print('post is already in like_posts')
                user.like_posts.remove(post)
                post.like_count -= 1
                post.save()
            else:
                # print('post is not in like_posts')
                user.like_posts.add(post)
                post.like_count += 1
                post.save()
            self.data = {
                'success': True,
                'like_count': post.like_count,
                'user_id': self.user_id,
                'post_id': self.post_id,
            }
        else:
            self.data = {
                'success': False,
            }

    def make_data(self):
        self._like_post();
        return self.data


class BlindPost:
    def __init__(self, request):
        self.post_id = request.data.get('postId', None)
        self.user_grade = request.data.get('userGrade', None)

    def _blind_post(self):
        # print('post/services.py > BlindPost self.user_grade is ', self.user_grade, type(self.user_grade))
        if self.post_id is not None:
            post = OdoqModels.Post.objects.get(id=self.post_id)
            post.blind = not post.blind
            post.blind_text = '관리자에 의해 블라인드 처리되었습니다.' if self.user_grade == 2 else post.blind_text
            post.save()
            self.data = {
                'success': True,
                'blind': post.blind,
                'blind_text': post.blind_text,
                'post_id': self.post_id,
            }
            # print('post/services.py > BlindPost self.data is ', self.data)
        else:
            self.data = {
                'success': False,
            }

    def make_data(self):
        self._blind_post()
        return self.data