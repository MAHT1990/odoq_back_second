from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from apscheduler.triggers.interval import IntervalTrigger
from django.db.models import Q
import odoq_models.models as OdoqModels
import api.question as Question
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
        self._get_phone_list(grade)
        if self.target_phone_list:
            for target_phone in self.target_phone_list:
                OdoqModels.SmsHistory.send_message(send_to=target_phone, is_auth=False, content=content)
            return {'success': True, 'message': '메시지 발송을 성공하였습니다.'}
        else:
            return {'success': False, 'message': '보낼 출제자가 존재하지 않습니다.'}

    def send_author_sms(self):
        # print('sendAuthorSMS called and current Question is ', self.question_data)
        self._get_question()
        solve_proposition = int((self.question_data['solve_count']/self.question_data['answer_count']*100)*100)/100
        try:
            content = f"(ODOQ)\n문항: {self.question_data['code']}\n답안수: {self.question_data['answer_count']}\n정답수: {self.question_data['solve_count']}\n정답률: {solve_proposition}%"
        except ZeroDivisionError:
            content = f"(ODOQ)\n문항: {self.qeustion_data['code']}\n답안수: {self.question_data['answer_count']}\n정답수: {self.question_data['solve_count']}\n정답률: 0%"
        return self._send_sms(content, 1)

    def send_student_sms(self):
        # print('sendStudentSMS called and current Question is ', self.question_data)
        content = f"(ODOQ) \n 새로운 문제가 업로드 되었습니다. https://odoq2.com/"
        return self._send_sms(content, 0)


def start_scheduler():
    scheduler = BackgroundScheduler()
    send_student_trigger = CronTrigger(day_of_week='mon-fri', hour=8, minute=30, second=10, jitter=3)
    send_author_trigger = CronTrigger(day_of_week='mon-fri', hour=8, minute=25, second=10, jitter=3)

    # test_interval_trigger = IntervalTrigger(seconds=30)

    # scheduler.add_job(SendSMS().send_author_sms,
    #                   trigger=test_interval_trigger,
    #                   id='test_message',
    #                   replace_existing=True)

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
