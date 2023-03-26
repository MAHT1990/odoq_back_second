import odoq_models.models as OdoqModels

class GetNotice:
    def __init__(self, request):
        self.request = request

    def make_data(self):
        notice = OdoqModels.Notice.objects.all().first()
        # print('api/notice/services.py > GetNotice is ', notice)
        # print(notice.season)
        # print(notice.img, type(notice.img))
        # print(notice.text)

        data = {
            'season': notice.season,
            'img_url': notice.img.url,
            'text': notice.text,
        } if notice is not None else {}
        return data