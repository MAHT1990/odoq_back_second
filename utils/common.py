import json
import math
import os
import time

import numpy as np
import odoq_models.models as OdoqModels



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

    print(messages)
    return ','.join(np.array(messages).flatten()) if messages else ''
  else:
    return ''
