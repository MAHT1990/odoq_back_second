from rest_framework.views import APIView
from common._RES import makeResponse
from . import services


class QuestionView(APIView):
    def get(self, request):
        # print('getquestion called')
        result = services.GetQuestion(request).make_data()
        response = makeResponse(
            'success',
            'Question is successfully fetched',
            result,
        )
        return response

    def post(self, request):
        # print('postquestion called')
        result = services.AnswerPost(request).make_data()
        response = makeResponse(
            'success',
            'answer is successfully posted',
            result,
        ) if result else makeResponse(
            'fail',
            'answer is failed to post',
            result,
        )
        return response

    def patch(self, request):
        # print('cheat Answer')
        result = services.AnswerCheat(request).make_data()
        response = makeResponse(
            'success',
            'answer is successfully cheated',
            result,
        ) if result else makeResponse(
            'fail',
            'answer is failed to cheat',
            result,
        )
        return response


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