from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.combining import AndTrigger
from apscheduler.triggers.cron import CronTrigger
from django_apscheduler.jobstores import DjangoJobStore, register_events, register_job
from django.db.models import Q
import odoq_models.models as OdoqModels
import api.question as Question
from utils.common import get_author_phone_numbers, get_student_phone_numbers
import datetime


class SendSMS:
    def _get_question(self):
        self.question_data = Question.services.GetQuestion({}).make_data()

    def _get_phone_list(self, grade):
        """
        :param grade: 0: student, 1: author
        :return: list
        """
        target_phone_query_set = OdoqModels.User.objects.filter(Q(grade=grade) | Q(grade=2), accept_sms=True)
        target_phone_list = [user.phone for user in target_phone_query_set]
        self.target_phone_list = target_phone_list

    def _send_sms(self, content, grade):
        """
        description: send sms to target phone list
        :param content: str
        :param grade: 0: student, 1: author
        :return: dict
        """
        self._get_question()
        if self.question_data:
            self._get_phone_list(grade)
            if self.target_phone_list:
                for target_phone in self.target_phone_list:
                    OdoqModels.SmsHistory.send_message(send_to=target_phone, is_auth=False, content=content)
                return {'success': True, 'message': '메시지 발송을 성공하였습니다.'}
            else:
                return {'success': False, 'message': '보낼 출제자가 존재하지 않습니다.'}
        else:
            return {'success': False, 'message': '문제가 존재하지 않습니다.'}

    def send_author_sms(self):
        # print('sendAuthorSMS called and current Question is ', self.question_data)
        try:
            content = f"(ODOQ)\n문항: {self.question_data['code']}\n답안수: {self.question_data['answer_count']}\n정답수: {self.question_data['solve_count']}\n정답률: {self.question_data['solve_count']/self.question_data['answer_count']*100}%"
        except ZeroDivisionError:
            content = f"(ODOQ)\n문항: {self.qeustion_data['code']}\n답안수: {self.question_data['answer_count']}\n정답수: {self.question_data['solve_count']}\n정답률: 0%"
        return self._send_sms(content, 1)

    def send_student_sms(self):
        # print('sendStudentSMS called and current Question is ', self.question_data)
        content = f"(ODOQ) \n 새로운 문제가 업로드 되었습니다. https://odoq2.com/"
        return self._send_sms(content, 0)

    def _get_test_message(self):
        self.test = datetime.datetime.now()

    def print_test_message(self):
        self._get_question()
        self._get_test_message()
        # print('question_data', self.question_data)
        # print('test message', self.test)


def start_scheduler():
    scheduler = BackgroundScheduler()
    send_student_trigger = CronTrigger(day_of_week='mon-fri', hour=2, minute=5, second=15, jitter=10)
    send_author_trigger = CronTrigger(day_of_week='mon-fri', hour=23, minute=59, second=00, jitter=30)

    scheduler.add_job(SendSMS().send_student_sms,
                      trigger=send_student_trigger,
                      id='send_student_sms',
                      replace_existing=True)
    scheduler.add_job(SendSMS().send_author_sms,
                      trigger=send_author_trigger,
                      id='send_author_sms',
                      replace_existing=True)
    # scheduler.add_job(SendSMS().print_test_message, 'interval', seconds=10, id='test_message')
    scheduler.start()
