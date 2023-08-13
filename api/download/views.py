from rest_framework.views import APIView
from common._RES import make_response
from django.conf import settings
from django.http import FileResponse
import os

class DownloadView(APIView):
    def get(self, request):
        # print('getdownload called')
        # print(request.GET.get('path', None))
        # print('MEDIA_ROOT is ', settings.MEDIA_ROOT)
        file_path = os.path.join(settings.MEDIA_ROOT, request.GET.get('path', None))
        # print('file_path is ', file_path)

        response = FileResponse(open(file_path, 'rb'))
        response['Content-Disposition'] = 'attachment; filename=' + request.GET['path'].split('/')[-1]
        response['Content-Type'] = 'application/octet-stream'

        return response
