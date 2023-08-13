import random
import string
import json
import datetime
from rest_framework.views import APIView
from rest_framework.response import Response

from common._CSRF import _CSRF
from common._RES import make_response

class TokenViewSet(APIView):
  def get(self, request):
    unique_id = ''.join(random.choices(
        string.ascii_uppercase + string.digits, k=32))

    response = make_response(
        'status', 'message', {
            'csrf_token': _CSRF.generateToken(unique_id),
            'csrf_uniqueid': unique_id,
            'csrf_expired': datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(minutes=10),
        })
    return response

  def post(self, request):
    csrf_token = ''
    unique_id = ''
    try:
      csrf_token = request.META["HTTP_X_CSRFTOKEN"]
      unique_id = request.META["HTTP_X_CSRFUNIQUEID"]
    except:
      try:
        csrf_token = json.loads(request.body)["csrf_token"]
        unique_id = json.loads(request.body)["csrf_uniqueid"]
      except:
        csrf_token = ''

    reason = ''
    if csrf_token != '' and unique_id != '':
      reason = '' if _CSRF.validateToken(
          csrf_token, unique_id) else 'BAD TOKEN OR EXPIRED'
    else:
      reason = 'No CSRF TOKEN OR Unique Id PRESENT'


    response = make_response(
        ('success' if reason == '' else 'error'),
        reason,
        data={}
    )
    return response
