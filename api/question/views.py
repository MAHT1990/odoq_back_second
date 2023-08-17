from rest_framework.views import APIView
from common._RES import make_response
from . import services


class QuestionView(APIView):
    def get(self, request):
        # print('QuestionService called')
        service_response = services.QuestionService(request).make_data()
        return make_response(
            'success' if service_response['success'] else 'fail',
            'Question is successfully fetched',
            service_response['data'],
        )

    def post(self, request):
        # print('postquestion called')
        service_response = services.AnswerSubmitService(request).make_data()
        if service_response['success']:
            result = 'success'
            message = 'answer is successfully posted'
            data = service_response['data']
        else:
            result = 'fail'
            message = 'answer is failed to post'
            data = service_response['data']
        return make_response(result, message, data)

    def patch(self, request):
        # print('cheat Answer')
        service_response = services.AnswerCheatService(request).make_data()
        result, message, data = (
            'success', 'answer is successfully cheated', service_response['data']
        ) if service_response['success'] else (
            'fail', 'answer is failed to cheat', service_response['data']
        )
        return make_response(result, message, data)


class AnswerView(APIView):
    def post(self, request):
        # print('postquestion called')
        service_response = services.AnswerSubmitService(request).make_data()
        result, message, data = (
            'success', 'answer is successfully posted', service_response['data']
        ) if service_response['data'] else (
            'fail', 'answer is failed to post', service_response['data']
        )
        return make_response(result, message, data)

    def patch(self, request):
        # print('cheat Answer')
        service_response = services.AnswerCheatService(request).make_data()
        result, message, data = (
            'success', 'answer is successfully cheated', service_response['data']
        ) if service_response['data'] else (
            'fail', 'answer is failed to cheat', service_response['data']
        )
        return make_response(result, message, data)


class AnswerHistoryView(APIView):
    def get(self, request):
        # print('AnswerHistoryService called')
        service_response = services.AnswerHistoryService(request).make_data()
        return make_response(
            'success' if service_response['success'] else 'fail',
            'AnswerHistory is successfully fetched',
            service_response['data'],
        )


class AnswerLiveView(APIView):
    def get(self, request):
        # print('AnswerLiveService called')
        service_response = services.AnswerLiveService(request).make_data()
        return make_response(
            'success' if service_response['success'] else 'fail',
            'AnswerLive is successfully loaded',
            service_response['data'],
        )
