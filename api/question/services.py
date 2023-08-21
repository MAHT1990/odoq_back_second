import odoq_models.models as OdoqModels
from common._RES import service_response
import datetime


USER_MODEL = OdoqModels.User
QUESTION_MODEL = OdoqModels.Question
ANSWER_HISTORY_MODEL = OdoqModels.AnswerHistory
SMS_HISTORY_MODEL = OdoqModels.SmsHistory


class QuestionService:
    now_utc = datetime.datetime.now(tz=datetime.timezone.utc)
    now_kor = datetime.datetime.now(tz=datetime.timezone(datetime.timedelta(hours=9)))
    _data = None
    _question = None
    _scnd_remain = None

    def __init__(self, request):
        self._request = request
        self._qs_qstn = QUESTION_MODEL.objects.all()

    def __get_remain_scnd_and_q(self, question):
        return abs((question.upload_datetime - self.now_utc).total_seconds()), question

    def __get_question(self):
        """
        현재 공개할 문제와, 다음 문제에의 남은시간
        :return: dict
        """
        if len(self._qs_qstn) > 0:
            try:
                list_question_current_and_next = [
                    min(list(map(self.__get_remain_scnd_and_q, qs)), key=lambda x: x[0])
                    for qs in [
                            self._qs_qstn.filter(upload_datetime__lte=self.now_utc),
                            self._qs_qstn.filter(upload_datetime__gte=self.now_utc)
                        ]
                ]
                self._question = list_question_current_and_next[0][1]
                self._scnd_remain = list_question_current_and_next[1][0]
            except ValueError as e:
                # print(e)
                self._question = min(list(map(self.__get_remain_scnd_and_q,
                            self._qs_qstn.filter(
                                upload_datetime__lte=self.now_utc
                            ))), key=lambda x: x[0])[1]
                self._scnd_remain = None
        else:
            self._question, self._scnd_remain = None, None

    def make_data(self):
        self.__get_question()
        try:
            data = {
                'id': self._question.id,
                'code': self._question.code,
                'season': self._question.season,
                'img_url': self._question.img.url,
                'answer': self._question.answer,
                'answer_count': self._question.answer_count,
                'solve_count': self._question.solve_count,
                'second_remain': self._scnd_remain,
                'solved_users': self._question.get_solved_users_list(),
                'cheated_users': self._question.get_cheated_users_list(),
            }
        except AttributeError as e:
            # print(e)
            data = None
        # print('api/question/services.py > QuestionService > self.data', self._data)
        return service_response(True if data else False, data)


class AnswerHistoryService:
    def __init__(self, request):
        self._request = request
        self.user_id = request.GET.get('userId', None)\
            if request.GET.get('userId', None) != '0' else None
        self.question_id = request.GET.get('questionId', None)\
            if request.GET.get('questionId', None) != '0' else None

        self.user = USER_MODEL.get_user_by_id(self.user_id)
        self.question = QUESTION_MODEL.get_question_by_id(self.question_id)

    def _get_answer_history(self):
        if self.user is not None and self.question is not None:
            try:
                self.answer_history = ANSWER_HISTORY_MODEL.objects.filter(
                    user=self.user,
                    question=self.question,
                ).order_by('-created_at')
            except ANSWER_HISTORY_MODEL.DoesNotExist as e:
                # print(e)
                self.answer_history = None

    def _get_has_solved_in_limit(self):
        if hasattr(self, 'answer_history'):
            if self.answer_history is not None:
                self.has_solved_in_limit = self.answer_history.filter(
                    isSolved=True,
                    over_limit=False,
                ).exists()
            else:
                self.has_solved_in_limit = False
        else:
            self.has_solved_in_limit = False

    def _get_can_answer_remain_time(self):
        if hasattr(self, 'answer_history'):
            if self.answer_history is not None:
                can_answer_remain_time = \
                    (30 * len(self.answer_history) - 15) - (
                            datetime.datetime.now(tz=datetime.timezone.utc) - self.answer_history[0].created_at
                    ).total_seconds() if len(self.answer_history) > 0 else 0
                self.can_answer_remain_time = can_answer_remain_time if can_answer_remain_time > 0 else 0
            else:
                self.can_answer_remain_time = 0
        else:
            self.can_answer_remain_time = 0

    def _get_wrong_answer_history(self):
        if hasattr(self, 'answer_history'):
            if self.answer_history is not None:
                self.wrong_answer_history = self.answer_history.filter(
                    isSolved=False,
                    over_limit=False,
                )
            else:
                self.wrong_answer_history = None
        else:
            self.wrong_answer_history = None
        # print('api/question/services.py > AnswerHistoryService > self.wrong_answer_history', self.wrong_answer_history)

    def make_data(self):
        self._get_answer_history()
        self._get_has_solved_in_limit()
        self._get_wrong_answer_history()
        self._get_can_answer_remain_time()
        data = {
            'user_not_exist': self.user_not_exist if hasattr(self, 'user_not_exist') else False,
            'has_solved_in_limit': self.has_solved_in_limit,
            'can_answer_remain_time': self.can_answer_remain_time,
            'wrong_answer_count': len(self.wrong_answer_history) if self.wrong_answer_history is not None else 0,
            'answer_history': [
                {
                    'id': answer_history.id,
                    'answer': answer_history.answer,
                    'isSolved': answer_history.isSolved,
                    'created_at': answer_history.created_at,
                } for answer_history in self.answer_history
            ] if self.wrong_answer_history is not None else None,
        }
        # print(data)
        return service_response(True if data else False, data)


class AnswerLiveService:
    def __init__(self, request):
        self._request = request
        if request.GET.get('questionId', None) != '0':
            self.question_id = request.GET.get('questionId', None)
        else:
            self.question_id = None

    def _get_answer_live(self):
        if self.question_id is not None:
            question = QUESTION_MODEL.objects.get(id=self.question_id)
            self.answer_live = ANSWER_HISTORY_MODEL.objects.filter(
                question=question,
            ).order_by('-created_at')
        else:
            self.answer_live = None

    def make_data(self):
        self._get_answer_live()
        if self.answer_live is not None:
            data = {
                'answers': [
                    {
                        'user_name': answer.user.name,
                        'user_grade': answer.user.grade,
                        'user_level': answer.user.get_user_level(),
                        'answer': answer.answer,
                        'is_solved': answer.isSolved,
                        'created_at': answer.created_at,
                        'over_limit': answer.over_limit,
                    } for answer in self.answer_live
                ]
            }
        else:
            data = None
        return service_response(True if data else False, data)


class AnswerCheatService:
    def __init__(self, request):
        self._request = request
        self.question_id = request.data.get('questionId', None)
        self.user_id = request.data.get('userId', None)

    def _answer_cheat(self):
        question = QUESTION_MODEL.get_question_by_id(self.question_id)
        user = USER_MODEL.objects.get(id=self.user_id)
        user.cheated_questions.add(question)
        user.save()
        self._cheated_users = question.get_cheated_users_list()

    def make_data(self):
        if self.question_id is None or self.user_id is None:
            return None

        self._answer_cheat()
        data = {
            'cheated_users': self._cheated_users,
        }
        return service_response(True if data else False, data)


class AnswerSubmitService:
    ANSWER_COUNT_LIMIT = 5

    def __init__(self, request):
        self._request = request
        self._question_id = request.data.get('questionId', None)
        self._user_id = request.data.get('userId', None)
        self._answer = request.data.get('answer', None)

        self.question = QUESTION_MODEL.get_question_by_id(self._question_id)
        self.user = USER_MODEL.get_user_by_id(self._user_id)

    def __is_cheated(self):
        return True if self.question.id in self.user.cheated_questions.all().values_list('id', flat=True) else False

    def __sms_first_solved_answer(self):
        question_solve_history = ANSWER_HISTORY_MODEL.objects.filter(
            question=self.question,
            answer=self.question.answer,
        ).order_by('-created_at')

        # 해당 question의 첫번째 답안일 경우에는 문자를 보낸다.
        if len(question_solve_history) == 1:
            for phone_number in USER_MODEL.get_author_phone_numbers():
                SMS_HISTORY_MODEL.send_message(
                    send_to=phone_number,
                    is_auth=False,
                    content=f'첫번째 정답이 등록되었습니다.\n{self.user.name}\n{self.user.phone}'
                )

    def __cal_remain_time(self):
        cal_remain_time = (30 * len(self.question_user_history) - 15) - (
                datetime.datetime.now(tz=datetime.timezone.utc) - self.question_user_history[0].created_at
        ).total_seconds()
        return cal_remain_time if cal_remain_time > 0 else 15

    def _answer_post(self):
        if self.question is None or self.user is None:
            self.data = None
            return

        # 미리보기 사용한 경우, 응답 만들어서 바로 return
        if self.__is_cheated():
            self._can_answer_remain_time = 15
            return

        new_history = ANSWER_HISTORY_MODEL.objects.create(
            question=self.question, user=self.user, answer=self._answer,
            isSolved=self.question.answer == self._answer,
        )
        self.question_user_history = ANSWER_HISTORY_MODEL.objects.filter(
            question=self.question, user=self.user,
        )

        """
        해당 문항에 현재 학생이 제출한 답안이 5회 이하일 경우에만 반영.
        해당 문항을 현재 학생이 이미 풀었을 경우에는 반영하지 않음.
        """

        if len(self.question_user_history) <= self.ANSWER_COUNT_LIMIT and self.question not in self.user.solved_questions.all():
            self.question.answer_count += 1
            self.user.answered_questions.add(self.question)

            if self.question.answer == self._answer:
                self.question.solve_count += 1
                self.user.solved_questions.add(self.question)
                self.__sms_first_solved_answer()
            else:
                self._can_answer_remain_time = self.__cal_remain_time()
            self.question.save(), self.user.save()

        elif len(self.question_user_history) > self.ANSWER_COUNT_LIMIT:
            # 5회 초과
            self.user.answered_questions.add(self.question)
            new_history.over_limit = True

            if self.question.answer == self._answer:
                self.user.solved_questions.add(self.question)
            else:
                self._can_answer_remain_time = self.__cal_remain_time()
            self.user.save(), new_history.save()
        else:
            # 5회 이하 && 이미 맞춘 문제.
            self._can_answer_remain_time = self.__cal_remain_time()

    def make_data(self):
        self._answer_post()
        data = {
            'is_written': False if self.__is_cheated() else True,
            'answer_count': self.question.answer_count,
            'solve_count': self.question.solve_count,
            'can_answer_remain_time': self._can_answer_remain_time,
            'solved_users': self.question.get_solved_users_list(),
        }
        return service_response(True if data else False, data)
