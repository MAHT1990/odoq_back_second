import odoq_models.models as OdoqModels
from django.core.paginator import Paginator

class GetPost:
    def __init__(self, request):
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
                'user': post.user.name,
                'content': post.content,
                'like_count': post.like_count,
                'created_at': post.created_at,
                'updated_at': post.updated_at,
                'blind': post.blind,
                'blind_text': post.blind_text,
            })
        pagenation = Paginator(list_temp_posts, self.page_size)
        list_result_posts = pagenation.page(self.page_number).object_list
        self.data['posts'] = list_result_posts

    def make_data(self):
        self._get_dict_posts()
        # print(self.data)
        return self.data