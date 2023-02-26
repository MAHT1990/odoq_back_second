import odoq_models.models as OdoqModels
import datetime

class GetQuestion:
    def __init__(self, request):
        self.request = request

    def _get_question(self):
        '''
        현재 공개할 문제와, 다음 문제에의 남은시간
        '''
        now_kor = datetime.datetime.now(tz=datetime.timezone(datetime.timedelta(hours=9)))
        now_weekday_kor = now_kor.weekday()
        now_utc = datetime.datetime.now(tz=datetime.timezone.utc)

        queryset_question = OdoqModels.Question.objects.all()
        # TODO: 없으면 None으로 잡히고, None의 attribute 접근에 대하여 AttributeError
        if len(queryset_question) > 0:
            try:
                list_question_current_and_next = [
                    min(
                        list(
                            map(
                                lambda q: (abs(round((now_utc - q.upload_datetime).total_seconds())), q),
                                qs
                            )
                        ),
                        key=lambda x: x[0]
                    ) for qs in [
                        queryset_question.filter(
                            upload_datetime__lte=now_utc
                        ),
                        queryset_question.filter(
                            upload_datetime__gte=now_utc
                        )
                    ]
                ]

                self.question = list_question_current_and_next[0][1]
                self.second_remain = list_question_current_and_next[1][0]
            except ValueError as e:
                # print(e)
                self.question = min(
                    list(
                        map(
                            lambda q: (abs(round((now_utc - q.upload_datetime).total_seconds())), q),
                            queryset_question.filter(
                                upload_datetime__lte=now_utc
                            )
                        )
                    ), key=lambda x: x[0]
                )[1]
                self.second_remain = None
        else:
            self.question, self.second_remain = None, None


    def make_data(self):
        self._get_question()
        try:
            self.data = {
                'code': self.question.code,
                'season': self.question.season,
                'img_url': self.question.img.url,
                'answer': self.question.answer,
                'answer_count': self.question.answer_count,
                'solve_count': self.question.solve_count,
                'second_remain': self.second_remain,
            }
        except AttributeError as e:
            # print(e)
            self.data = None
        # print(self.data)
        return self.data

