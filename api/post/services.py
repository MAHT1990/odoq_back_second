import odoq_models.models as OdoqModels
import datetime
from django.core.paginator import Paginator

class GetPost:
    def __init__(self, request):
        # print('request.GET in post.services is ', request.GET)
        self.request = request
        self.page_number = request.GET.get('pageNumber', 1)
        self.page_size = request.GET.get('pageSize', 7)
        self.filtering_flag = request.GET.get(
            'filteringFlag',
            request.data.get('filteringFlag', 'all')
        )
        self.ordering_flag = request.GET.get('orderingFlag', 'latest')
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
                'user_name': post.user.name,
                'content': post.content,
                'like_count': post.like_count,
                'liked_users': [user.id for user in post.liked_users.all()],
                'created_at': post.created_at + datetime.timedelta(hours=9),
                'updated_at': post.updated_at + datetime.timedelta(hours=9),
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
            self.data['today_posts'] = len(list(filter(lambda x: x['created_at'].date() == datetime.date.today(), self.posts)))
        except :
            # TODO: 아마도 today_posts에서 예외처리가 필요할 수도.
            # print('EmptyPage')
            pass
        # print(self.data)
        return self.data

class LikePost:
    def __init__(self, request):
        # print('request.data in likePost is ', request.data)
        self.post_id = request.data.get('postId', None)
        self.user_id = request.data.get('userId', None)

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