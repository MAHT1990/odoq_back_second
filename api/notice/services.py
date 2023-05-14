import odoq_models.models as OdoqModels

class GetNotice:
    def __init__(self, request):
        self.request = request

    def make_data(self):
        notices = OdoqModels.Notice.objects.all()
        # print('api/notice/services.py > GetNotice is ', notice)
        # print(notice.season)
        # print(notice.img, type(notice.img))
        # print(notice.text)

        data = {
            'notices': [{
                'id': notice.id,
                'title': notice.title,
                'img_url': notice.img.url,
                'text': notice.text,
                'created_at': notice.created_at,
                'updated_at': notice.updated_at,
            } for notice in notices if notice is not None]
        }
        return data