import sched, time
from utils import common
from datetime import datetime, timedelta
import odoq_models.models as OdoqModels
import api.question as Question
import threading

class SendSMS():
    def __init__(self):
        self.question_data = Question.services.GetQuestion({}).make_data()
        self.target_phone_list = []

    def _get_phone_list(self, grade):
        '''
        :param grade: 0: student, 1: author
        '''
        target_phone_query_set = OdoqModels.User.objects.filter(grade=grade)
        target_phone_list = [user.phone for user in target_phone_query_set]
        self.target_phone_list = target_phone_list

    def _send_sms(self, content):
        for target_phone in self.target_phone_list:
            OdoqModels.SmsHistory.send_message(send_to=target_phone, is_auth=False, content=content)

    def send_author_sms(self):
        print('sendAuthorSMS called and current Question is ', self.question_data)
        if self.question_data:
            self._get_phone_list(1)
            if self.target_phone_list:
                content = f"제출 답안수는 {self.question_data['answer_count']} 입니다."
                self._send_sms(content)
                return {'success': True, 'message': '메시지 발송을 성공하였습니다.'}
            else:
                return {'success': False, 'message': '보낼 출제자가 존재하지 않습니다.'}
        else:
            return {'success': False, 'message': '문제 Data가 존재하지 않습니다.'}

    def send_student_sms(self):
        print('sendStudendSMS called and current Question is ', self.question_data)
        if self.question_data:
            self._get_phone_list(0)
            if self.target_phone_list:
                content = f"제출 답안수는 {self.question_data['answer_count']} 입니다."
                self._send_sms(content)
                return {'success': True, 'message': '메시지 발송을 성공하였습니다.'}
            else:
                return {'success': True, 'message': None}
        else:
            return {'success': False, 'message': '문제 Data가 존재하지 않습니다.'}


def start_scheduler():
    sms_scheduler = sched.scheduler(time.time, time.sleep)

    def send_sms():
        # send sms every 23:55pm
        now = datetime.now()
        target_time = datetime(now.year, now.month, now.day, 23, 59, 55)
        if now > target_time:
            target_time += timedelta(days=1)
        SendSMS().send_author_sms()
        SendSMS().send_student_sms()
        sms_scheduler.enter((target_time - now).total_seconds(), 1, send_sms)

    sms_scheduler.enter(10, 1, send_sms)
    thread = threading.Thread(target=sms_scheduler.run)
    thread.daemon = True
    thread.start()

def start_test_scheduler():
    test_scheduler = sched.scheduler(time.time, time.sleep)

    def print_message():
        test_scheduler.enter(10, 1, print_message)
        print('test_scheduler is working duruduru', time.time(), threading.current_thread().name)
    def scheduler_thread():
        test_scheduler.run()

    print('test_scheduler is started', time.time())
    print('test_scheduler\'s queue is ', test_scheduler.queue)
    test_scheduler.enter(10, 1, print_message)
    thread = threading.Thread(target=scheduler_thread)
    thread.daemon = True
    thread.start()


