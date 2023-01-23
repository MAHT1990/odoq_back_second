from django.http import JsonResponse
from rest_framework.views import APIView

def index(request):
    return JsonResponse({
        'test': 'test',
    })


