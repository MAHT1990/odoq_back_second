from rest_framework.views import APIView
from common._RES import make_response
from . import services


class QuestionView(APIView):
    def get(self, request):
        # print('QuestionService called')
        data = services.QuestionService(request).make_data()
        response = make_response(
            result='success',
            message='Question is successfully fetched',
            data=data,
        )
        return response

    def post(self, request):
        # print('postquestion called')
        data = services.AnswerSubmitService(request).make_data()
        result, message, data = (
            'success', 'answer is successfully posted', data
        ) if data else (
            'fail', 'answer is failed to post', data
        )
        return make_response(result, message, data)

    def patch(self, request):
        # print('cheat Answer')
        data = services.AnswerCheat(request).make_data()
        result, message, data = (
            'success', 'answer is successfully cheated', data
        ) if data else (
            'fail', 'answer is failed to cheat', data
        )
        return make_response(result, message, data)


class AnswerView(APIView):
    def post(self, request):
        # print('postquestion called')
        data = services.AnswerSubmitService(request).make_data()
        result, message, data = (
            'success', 'answer is successfully posted', data
        ) if data else (
            'fail', 'answer is failed to post', data
        )
        return make_response(result, message, data)

    def patch(self, request):
        # print('cheat Answer')
        data = services.AnswerCheatService(request).make_data()
        result, message, data = (
            'success', 'answer is successfully cheated', data
        ) if data else (
            'fail', 'answer is failed to cheat', data
        )
        return make_response(result, message, data)

class AnswerHistoryView(APIView):
    def get(self, request):
        # print('AnswerHistoryService called')
        result = services.AnswerHistoryService(request).make_data()
        # print('AnswerHistory get result is ', result)
        response = make_response(
            'success',
            'AnswerHistory is successfully fetched',
            result,
        )
        return response


class AnswerLiveView(APIView):
    def get(self, request):
        # print('AnswerLiveService called')
        result = services.AnswerLiveService(request).make_data()
        # print('AnswerLive get result is ', result)
        response = make_response(
            'success',
            'AnswerLive is successfully loaded',
            result,
        )
        return response