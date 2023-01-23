import odoq_models.models as OdoqModels
import datetime

class GetQuestion:
    def __init__(self, request):
        self.request = request
    def _get_question(self, *args, **kwargs):
        self.question = OdoqModels.Question.objects.all().first()

    def make_data(self):
        self._get_question()
        self.data = {
            'code': self.question.code,
            'season': self.question.season,
            'img_url': self.question.img.url,
            'answer': self.question.answer,
            'answer_count': self.question.answer_count,
            'solve_count': self.question.solve_count,
        }
        return self.data

# def get_current_qeustion(request):
#     seoul_timezone = datetime.timezone(9)
#     now_kor = datetime.now(tz=seoul_timezone)
#     now_weekday_kor = now_kor.weekday()
#     now_utc = datetime.now(tz=datetime.timezone.utc)
#
#     # question_queryset = OdoqModels.Question.objects.all().first()
#
#     data = {
#         'img': test_question.img
#     }
#
#     # question_current = None
#     # question_next = None
#     # question_next_countdown = None
#
#     return data

