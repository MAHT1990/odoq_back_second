import odoq_models.models as OdoqModels

class GetPost:
    def __init__(self, request):
        self.request = request

    def _get_post(self):
        queryset_post = OdoqModels.Post.objects.all()
        self.post = queryset_post
    def make_data(self):
        self._get_post()
        self.data = {

        }
        print(self.data)
        return self.data