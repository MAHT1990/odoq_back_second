from common._RES import midResponse
from common._JWT import JWT
import jwt
from django.http import JsonResponse, HttpResponse


class JWTDecorator:
  def __init__(self, origin_func):
    self.origin_func = origin_func

  def __call__(self, request, *args, **kwargs):
    if ('X-JWT' in request.headers):
      try:
        request.decoded = JWT.decode(request.headers["X-JWT"])

        # TODO grade 확인하여 허용/불가 처리 하기...
        return self.origin_func(self, request, *args, **kwargs)
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


class JWTDecoratorForNonMember:  # 비회원 인증 (비회원 주문조회 용)
  def __init__(self, origin_func):
    self.origin_func = origin_func

  def __call__(self, request, *args, **kwargs):
    if 'X-JWTNONMEMBER' in request.headers:
      try:
        request.decoded = JWT.decode(request.headers['X-JWTNONMEMBER'])

        return self.origin_func(self, request, *args, **kwargs)
      except jwt.ExpiredSignatureError:
        return midResponse(
          result='error',
          message='NonMember JWT Expired!',
          data={
            'grade': 0,  # grade: user
          },
          error_code=461,
        )
      except jwt.exceptions.DecodeError:
        return midResponse(
            result='error',
            message='NonMember JWT DecodeError!',
            error_code=460,
        )
    else:
      return midResponse('error', 'NO NonMember JWT!')


class JWTMiddleWare:
  def __init__(self, next_layer=None):
    self.get_response = next_layer
    self.exclude_path_list = [
      '/api/v1/csrf/',
      '/api/v1/admin/user/login'
    ]

  def process_request(self, request):
    print(request.path)
    # ! 만약 제외해야될 위치가 있다면 여기에서 제외
    if request.path in self.exclude_path_list:
      return None

    if ('X-JWT' in request.headers):
      try:
        request.decoded = JWT.decode(request.headers["X-JWT"])

        # TODO grade 확인하여 허용/불가 처리 하기...
        return None
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
