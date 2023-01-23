from common._RES import midResponse
from common._JWT import JWT
import jwt
from common._CSRF import _CSRF


def cross_decorator(func):
  def check(self, request, *args, **kwargs):
    if 'X-JWT' in request.headers:
      try:
        request.decoded = JWT.decode(request.headers["X-JWT"])
        request.decoded['user_id'] = request.decoded['info'].split('_')[0]
        request.decoded['user_grade'] = request.decoded['info'].split('_')[1]
        request.decoded['store_id'] = request.decoded['info'].split('_')[2]

        if 'X-CSRFTOKEN' in request.headers and 'X-CSRFUNIQUEID' in request.headers:
          csrf_token = request.headers['X-CSRFTOKEN']
          csrf_unique_id = request.headers['X-CSRFUNIQUEID']
          if _CSRF.validateToken(csrf_token, csrf_unique_id):
            return func(self, request, *args, **kwargs)
          else:
            return midResponse('error', 'CSRF TOKEN VALIDATION FAILED', error_code=406)
        else:
          return midResponse('error', 'NO CSRF TOKEN FOUND', error_code=405)
      except jwt.ExpiredSignatureError:
        decode = JWT.decode(request.headers["X-JWT"], verify=False)

        return midResponse(
            result='error',
            message='JWT Expired!',
            data={
                'grade': decode['info'].split('_')[1]
            },
            error_code=461,
        )
      except jwt.exceptions.DecodeError:
        return midResponse(
            result='error',
            message='JWT DecodeError!',
            error_code=460,
        )
    else:
      return midResponse('error', 'NO JWT TOKEN FOUND', error_code=405)
      # JWT 인증 활성화시에 주석 해제해주어야합니다
      # return None

  return check


def cross_decorator_for_nonmember(func):
  def check(self, request, *args, **kwargs):
    if 'X-JWTNONMEMBER' in request.headers:
      try:
        request.decoded = JWT.decode(request.headers["X-JWTNONMEMBER"])
        request.decoded['email'] = request.decoded['info'].split('_')[0]
        request.decoded['phone'] = request.decoded['info'].split('_')[1]

        if 'X-CSRFTOKEN' in request.headers and 'X-CSRFUNIQUEID' in request.headers:
          csrfToken = request.headers['X-CSRFTOKEN']
          csrfUniqueId = request.headers['X-CSRFUNIQUEID']
          if (_CSRF.validateToken(csrfToken, csrfUniqueId)):
            return func(self, request, *args, **kwargs)
          else:
            return midResponse('error', 'CSRF TOKEN VALIDATION FAILED', error_code=406)
        else:
          return midResponse('error', 'NO CSRF TOKEN FOUND', error_code=405)
      except jwt.ExpiredSignatureError:
        decode = JWT.decode(request.headers["X-JWT"], verify=False)

        return midResponse(
          result='error',
          message='JWT Expired!',
          data={
            'grade': decode['info'].split('_')[1]
          },
          error_code=461,
        )
      except jwt.exceptions.DecodeError:
        return midResponse(
          result='error',
          message='JWT DecodeError!',
          error_code=460,
        )
    else:
      return midResponse('error', 'NO JWT!')
      # JWT 인증 활성화시에 주석 해제해주어야합니다
      # return None

  return check
