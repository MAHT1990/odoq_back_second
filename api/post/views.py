from rest_framework.views import APIView
from common._RES import makeResponse
from . import services, serializers

class PostView(APIView):
    def get(self, request):
        print('getPost get called')
        result = services.GetPost(request).make_data()
        response = makeResponse(
            'success',
            '',
            result,
        )
        return response

    def post(self, request):
        # print('createPost get called')
        # print('request.data is ', request.data)
        post_before_validated = serializers.PostSerializer(data=request.data)
        if post_before_validated.is_valid():
            post = post_before_validated.save()

        response = makeResponse(
            'status',
            'message',
            {}
        )
        return response