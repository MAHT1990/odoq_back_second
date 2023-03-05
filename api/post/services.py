import odoq_models.models as OdoqModels
from django.core.paginator import Paginator

class GetPost:
    def __init__(self, request):
        print('request.GET in post.services is ', request.GET)
        self.request = request
        self.page_number = request.GET.get('pageNumber', 1)
        self.page_size = request.GET.get('pageSize', 7)

        self.data = {
            'posts': [],
        }

    def _get_dict_posts(self):
        queryset_post = OdoqModels.Post.objects.all()
        list_temp_posts = []
        for post in queryset_post:
            list_temp_posts.append({
                'id': post.id,
                'user_id': post.user.id,
                'user_name': post.user.name,
                'content': post.content,
                'like_count': post.like_count,
                'liked_users': [user.id for user in post.liked_users.all()],
                'created_at': post.created_at,
                'updated_at': post.updated_at,
                'blind': post.blind,
                'blind_text': post.blind_text,
            })
        pagination = Paginator(list_temp_posts, self.page_size)
        try:
            list_result_posts = pagination.page(self.page_number).object_list
            self.data['posts'] = list_result_posts
            self.data['current_page'] = pagination.page(self.page_number).number
            self.data['total_pages'] = pagination.num_pages
            self.data['total_posts'] = pagination.count
        except :
            print('EmptyPage')

    def make_data(self):
        self._get_dict_posts()
        # print(self.data)
        return self.data

class LikePost:
    def __init__(self, request):
        print('request.data in likePost is ', request.data)
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