import json
import math
import os
import time

import numpy as np
import odoq_models.models as OdoqModels
from django.db.models import Q



# serializer error to message string
def serializer_error_message(errors):
  if errors:
    messages = []
    for error in list(errors.values()):
      if type(error) is dict:
        for item in list(error.values()):
          if type(item) is dict:
            for inItem in list(item.values()):
              messages.append(inItem)
          else:
            messages.append(item)
      else:
        messages.append(error)

    # print(messages)
    return ','.join(np.array(messages).flatten()) if messages else ''
  else:
    return ''

def get_author_phone_numbers():
  # get phone_numbers of authors or admin (grade = 1 or 2) and acceptSMS = True
  author_phone_numbers = OdoqModels.User.objects.filter(Q(grade=1) | Q(grade=2)).filter(accept_sms=True).values_list('phone', flat=True)

  return author_phone_numbers

def get_student_phone_numbers():
    # get phone_numbers of students (grade = 0) and accept_sms = True
    student_phone_numbers = OdoqModels.User.objects.filter(grade=0).filter(accept_sms=True).values_list('phone', flat=True)

    return student_phone_numbers