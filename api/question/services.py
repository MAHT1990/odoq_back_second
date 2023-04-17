import odoq_models.models as OdoqModels
import datetime
from utils.common import get_author_phone_numbers


class GetQuestion:
    def __init__(self, request):
        self.data = None
        self._request = request
        self._qs_qstn = OdoqModels.Question.objects.all()
        self._question = None
        self._scnd_remain = None

    def __get_remain_scnd_and_q(self, question):
        now_utc = datetime.datetime.now(tz=datetime.timezone.utc)
        return abs((question.upload_datetime - now_utc).total_seconds()), question

    def __get_question(self):
        """
        현재 공개할 문제와, 다음 문제에의 남은시간
        :return: dict
        """
        now_kor = datetime.datetime.now(tz=datetime.timezone(datetime.timedelta(hours=9)))
        now_utc = datetime.datetime.now(tz=datetime.timezone.utc)

        # TODO: 없으면 None으로 잡히고, None의 attribute 접근에 대하여 AttributeError

        if len(self._qs_qstn) > 0:
            try:
                list_question_current_and_next = [
                    min(list(map(self.__get_remain_scnd_and_q, qs)), key=lambda x: x[0])
                    for qs in [
                            self._qs_qstn.filter(upload_datetime__lte=now_utc),
                            self._qs_qstn.filter(upload_datetime__gte=now_utc)
                        ]
                ]

                self._question = list_question_current_and_next[0][1]
                self._scnd_remain = list_question_current_and_next[1][0]
            except ValueError as e:
                # print(e)
                self._question = min(list(map(self.__get_remain_scnd_and_q,
                            self._qs_qstn.filter(
                                upload_datetime__lte=now_utc
                            ))), key=lambda x: x[0])[1]
                self._scnd_remain = None
        else:
            self._question, self._scnd_remain = None, None

    def make_data(self):
        self.__get_question()
        try:
            self.data = {
                'id': self._question.id,
                'code': self._question.code,
                'season': self._question.season,
                'img_url': self._question.img.url,
                'answer': self._question.answer,
                'answer_count': self._question.answer_count,
                'solve_count': self._question.solve_count,
                'second_remain': self._scnd_remain,
            }
        except AttributeError as e:
            pass
        # print(self.data)
        # print('api/question/services.py > GetQuestion > self.data', self.data)
        return self.data


class GetAnswerHistory:
    def __init__(self, request):
        self._request = request
        if (request.GET.get('userId', None) != '0'):
            self.user_id = request.GET.get('userId', None)
        else:
            self.user_id = None
        if (request.GET.get('questionId', None) != '0'):
            self.question_id = request.GET.get('questionId', None)
        else:
            self.question_id = None
        # print('api/question/services.py > GetAnswerHistory > self.user_id, self.question_id', self.user_id, self.question_id)

    def _get_can_answer_remain_time(self):
        if self.user_id is not None and self.question_id is not None:
            user = OdoqModels.User.objects.get(id=self.user_id)
            question = OdoqModels.Question.objects.get(id=self.question_id)
            question_answer_history = OdoqModels.AnswerHistory.objects.filter(
                user=user,
                question=question,
            ).order_by('-created_at')
            can_answer_remain_time = \
                (30 * len(question_answer_history) - 15) - (
                        datetime.datetime.now(tz=datetime.timezone.utc) - question_answer_history[0].created_at
                ).total_seconds() if len(question_answer_history) > 0 else 0
            self.can_answer_remain_time = can_answer_remain_time if can_answer_remain_time > 0 else 0
        else:
            self.can_answer_remain_time = 0
        # print('api/question/services.py > GetAnswerHistory > self.can_answer_remain_time', self.can_answer_remain_time)

    def make_data(self):
        self._get_can_answer_remain_time()
        self.data = {
            'can_answer_remain_time': self.can_answer_remain_time,
        }
        # print(self.data)
        return self.data


class GetAnswerLive:
    def __init__(self, request):
        self._request = request
        if request.GET.get('questionId', None) != '0':
            self.question_id = request.GET.get('questionId', None)
        else:
            self.question_id = None

    def _get_answer_live(self):
        if self.question_id is not None:
            question = OdoqModels.Question.objects.get(id=self.question_id)
            self.answer_live = OdoqModels.AnswerHistory.objects.filter(
                question=question,
            ).order_by('-created_at')
        else:
            self.answer_live = None

    def make_data(self):
        self._get_answer_live()
        if self.answer_live is not None:
            self.data = {
                'answers': [
                    {
                        'user_name': answer.user.name,
                        'answer': answer.answer,
                        'is_solved': answer.isSolved,
                        'created_at': answer.created_at,
                    } for answer in self.answer_live
                ]
            }
        else:
            self.data = None

        return self.data


class AnswerPost:
    def __init__(self, request):
        self._request = request
        self.question_id = request.data.get('questionId', None)
        self.user_id = request.data.get('userId', None)
        self.answer = request.data.get('answer', None)

    def _answer_post(self):
        if self.question_id is not None and self.user_id is not None and self.answer is not None:
            question, user = OdoqModels.Question.objects.get(id=self.question_id), OdoqModels.User.objects.get(id=self.user_id)
            OdoqModels.AnswerHistory.objects.create(
                question=question,
                user=user,
                answer=self.answer,
                isSolved=question.answer == self.answer,
            )
            question_user_history = OdoqModels.AnswerHistory.objects.filter(
                question=question,
                user=user,
            )


            # print('api/question/services.py > AnswerPost > question_user_history', question_user_history)
            # 해당 question의 첫번째 답안일 경우에는 문자를 보낸다.
            # if len(question_user_history) == 0:
            #     OdoqModels.SmsHistory.send_message
            is_written = False
            can_answer_remain_time = 15 #seconds
            # print('api/question/services.py > AnswerPost > question, user', question, user)
            # print('api/question/services.py > AnswerPost > user.answered_questions', user.answered_questions.all())
            # print('api/question/services.py > AnswerPost > user.solved_questions', user.solved_questions.all())
            # print('api/question/services.py > AnswerPost > question_user_history', question_user_history)
            # print('api/question/services.py > AnswerPost > question_user_history.count()', question_user_history.count())
            # print('api/question/services.py > AnswerPost > len(question_user_history)', len(question_user_history))

            # 해당 문항에 현재 학생이 제출한 답안이 5회 이하일 경우에만 반영.
            # 해당 문항을 현재 학생이 풀었을 경우에는 반영하지 않음.
            if len(question_user_history) < 6 and question not in user.solved_questions.all():
                question.answer_count += 1
                user.answered_questions.add(question)
                is_written = True

                # print('## question.answer', question.answer)
                # print('## self.answer', self.answer)
                # print('## question.answer == self.answer', question.answer == self.answer)
                if question.answer == self.answer:
                    question.solve_count += 1
                    user.solved_questions.add(question)

                    question_solve_history = OdoqModels.AnswerHistory.objects.filter(
                        question=question,
                        answer=question.answer,
                    ).order_by('-created_at')
                    # print('## api/question/services.py > AnswerPost > question_solve_history', question_solve_history)

                    if len(question_solve_history) == 1:
                        # print('api/question/services.py > AnswerPost > question_solve_history', question_solve_history)
                        # print('첫번째 정답이 등록되었습니다')
                        for phone_number in get_author_phone_numbers():
                            OdoqModels.SmsHistory.send_message(
                                send_to=phone_number,
                                is_auth=False,
                                content=f'첫번째 정답이 등록되었습니다.\n{user.name}\n{user.phone}'
                            )
                else:
                    can_answer_remain_time = \
                        (30 * len(question_user_history) - 15) - (
                                datetime.datetime.now(tz=datetime.timezone.utc) - question_user_history[0].created_at
                        ).total_seconds()
                    if can_answer_remain_time < 0:
                        can_answer_remain_time = 0

                question.save(), user.save()

            else:
                can_answer_remain_time = \
                    (30 * len(question_user_history) - 15) - (
                                datetime.datetime.now(tz=datetime.timezone.utc) - question_user_history[0].created_at
                    ).total_seconds()
                if can_answer_remain_time < 0:
                    can_answer_remain_time = 0

            self.data = {
                'is_written': is_written,
                'answer_count': question.answer_count,
                'solve_count': question.solve_count,
                'can_answer_remain_time': can_answer_remain_time,
            }
        else:
            self.data = None

    def make_data(self):
        self._answer_post()
        return self.data