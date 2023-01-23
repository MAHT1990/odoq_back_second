from common._RES import midResponse

# GRADE 0 : 일반 유저 / 1 : 스토어 어드민 / 2 : 슈퍼 어드민
SUPERADMIN_GRADE = '2'


def superadmin_decorator(func):
  def check(self, request, *args, **kwargs):

    if not request.decoded:
      return midResponse('error', 'JWT DECODE ERROR', error_code=460)

    user_grade = request.decoded['info'].split('_')[1]
    if user_grade != SUPERADMIN_GRADE:
      return midResponse('error', 'SUPER ADMIN AUTHORIZATION FAILED', error_code=407)
    return func(self, request, *args, **kwargs)

  return check


