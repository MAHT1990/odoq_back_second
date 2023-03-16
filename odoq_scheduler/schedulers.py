from apscheduler.schedulers.background import BackgroundScheduler
from django_apscheduler.jobstores import DjangoJobStore, register_events, register_job
import odoq_models.models as OdoqModels
import api.question as Question
import datetime

class SendSMS():
    def __init__(self):
        self.question_data = Question.services.GetQuestion({}).make_data()
        self.target_phone_list = []

    def _get_question(self):
        self.question_data = Question.services.GetQuestion({}).make_data()
    def _get_phone_list(self, grade):
        '''
        :param grade: 0: student, 1: author
        '''
        target_phone_query_set = OdoqModels.User.objects.filter(grade=grade)
        target_phone_list = [user.phone for user in target_phone_query_set]
        self.target_phone_list = target_phone_list

    def _send_sms(self, content, grade):
        '''
        description: send sms to target phone list
        :param content: str
        :param grade: 0: student, 1: author
        '''
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
            content = f"답안수: {self.question_data['answer_count']}\n정답수: {self.question_data['solve_count']}\n정답률: {self.question_data['solve_count']/self.question_data['answer_count']*100}%"
        except ZeroDivisionError:
            content = f"답안수: {self.question_data['answer_count']}\n정답수: {self.question_data['solve_count']}\n정답률: 0%"
        return self._send_sms(content, 1)

    def send_student_sms(self):
        # print('sendStudentSMS called and current Question is ', self.question_data)
        content = f"(TEST)식사는 하셨습니까?"
        return self._send_sms(content, 0)

def print_test_message():
    print('test message', datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

def start_scheduler():
    scheduler = BackgroundScheduler()
    # scheduler.add_jobstore(DjangoJobStore(), "djangojobstore")
    scheduler.add_job(SendSMS().send_student_sms, replace_existing=True, trigger='cron', hour=12, minute=00, id='send_student_sms')
    scheduler.add_job(SendSMS().send_author_sms, replace_existing=True, trigger='cron', hour=23, minute=59, second=50, id='send_author_sms')
    register_events(scheduler)
    scheduler.start()


