import jwt
import datetime

JWT_SECRET_KEY = 'jflibvla!23n1klzbdE2j3io4!2nkvlEDnvk!2nalEW1'
JWT_ALGORITHM = 'HS256'

# GRADE 0 : 일반 유저 1 : 스토어 어드민 2 : 슈퍼 어드민

class JWT():
  @staticmethod
  def sign(id, grade, name):
    data = {}
    data['info'] = "{}_{}_{}".format(id, grade, name)
    data['exp'] = datetime.datetime.utcnow() + datetime.timedelta(days=3)
    # 토큰 유효시간 ( 기본 설정 3일 )
    return jwt.encode(data, JWT_SECRET_KEY, algorithm=JWT_ALGORITHM)

  @staticmethod
  def decode(data, verify=True):
    return jwt.decode(data, JWT_SECRET_KEY, algorithm=JWT_ALGORITHM, verify=verify)
