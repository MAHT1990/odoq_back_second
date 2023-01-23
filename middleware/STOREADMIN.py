from common._RES import midResponse

# 스토어 어드민 API 권한 확인
# Check Grade : [ 1(STORE), 2(SUPER) ]
# JWT 정책 : {user_id}_{grade}_{store_id}

CHECK_GRADE = ['1', '2']


def storeadmin_decorator(func):
  def check(self, request, *args, **kwargs):
    if not request.decoded:
      return midResponse('error', 'JWT DecodedError!', error_code=460)

    # check grade
    user_grade = request.decoded['info'].split('_')[1]
    store_id = request.decoded['info'].split('_')[2]
    if user_grade in CHECK_GRADE:
      if store_id:
        return func(self, request, *args, **kwargs)

    return midResponse('error', 'Invalid Grade Error!', error_code=460)

  return check
