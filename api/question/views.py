from rest_framework.views import APIView
from common._RES import makeResponse
from . import services


class QuestionView(APIView):
    def get(self, request):
        # print('QuestionService called')
        data = services.QuestionService(request).make_data()
        response = makeResponse(
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
        return makeResponse(result, message, data)

    def patch(self, request):
        # print('cheat Answer')
        data = services.AnswerCheat(request).make_data()
        result, message, data = (
            'success', 'answer is successfully cheated', data
        ) if data else (
            'fail', 'answer is failed to cheat', data
        )
        return makeResponse(result, message, data)


class AnswerHistoryView(APIView):
    def get(self, request):
        # print('getanswerhistory called')
        result = services.GetAnswerHistory(request).make_data()
        response = makeResponse(
            'success',
            'AnswerHistory is successfully fetched',
            result,
        )
        return response


class AnswerLiveView(APIView):
    def get(self, request):
        # print('getanswerlive called')
        result = services.GetAnswerLive(request).make_data()
        response = makeResponse(
            'success',
            'AnswerLive is successfully loaded',
            result,
        )
        return response