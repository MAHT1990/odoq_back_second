from common._RES import midResponse
from common._CSRF import _CSRF


def csrf_decorator(func):
  def check(self, request, *args, **kwargs):
    if 'X-CSRFTOKEN' in request.headers and 'X-CSRFUNIQUEID' in request.headers:
      csrf_token = request.headers['X-CSRFTOKEN']
      csrf_unique_id = request.headers['X-CSRFUNIQUEID']
      if _CSRF.validateToken(csrf_token, csrf_unique_id):
        return func(self, request, *args, **kwargs)
      else:
        return midResponse('error', 'CSRF TOKEN VALIDATION FAILED', error_code=406)

    else:
      return midResponse('error', 'NO CSRF TOKEN FOUND', error_code=405)
  return check


class CSRFMiddleWare:
  def __init__(self, next_layer=None):
    self.get_response = next_layer

  def process_request(self, request):
    if (request.method not in ['GET']):
      if ('X-CSRFTOKEN' in request.headers and 'X-CSRFUNIQUEID' in request.headers):
        csrfToken = request.headers['X-CSRFTOKEN']
        csrfUniqueId = request.headers['X-CSRFUNIQUEID']

        if (_CSRF.validateToken(csrfToken, csrfUniqueId)):
          return None
        else:
          return midResponse('error', 'CSRF TOKEN VALIDATION FAILED', error_code=406)
        return None
      else:
        return midResponse('error', 'NO CSRF TOKEN FOUND', error_code=405)

  def process_response(self, request, response):
    return response

  def __call__(self, request):
    response = self.process_request(request)
    if response is None:
        # If process_request returned None, we must call the next middleware or
        # the view. Note that here, we are sure that self.get_response is not
        # None because this method is executed only in new-style middlewares.
        response = self.get_response(request)
    response = self.process_response(request, response)
    return response
