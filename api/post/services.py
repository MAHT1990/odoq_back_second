import odoq_models.models as OdoqModels
from . import serializers

class GetPost:
    def __init__(self, request):
        self.request = request

        self.data = {
            'posts': [],
        }

    def _get_dict_posts(self):
        queryset_post = OdoqModels.Post.objects.all()
        # self.post = serializers.PostSerializer(data=queryset_post, many=True)
        for post in queryset_post:
            self.data['posts'].append({
                'id': post.id,
                'user': post.user.name,
                'content': post.content,
                'like_count': post.like_count,
                'created_at': post.created_at,
                'updated_at': post.updated_at,
                'blind': post.blind,
                'blind_text': post.blind_text,
            })


    def make_data(self):
        self._get_dict_posts()
        print(self.data)
        return self.data