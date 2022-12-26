import binascii
import csrf
import datetime
import string
import random

SERVER_SECRET = binascii.unhexlify(
    b"9e20abdbf8b24c91851170f2f0efebd64d732d86920bf0e2952fb18a6bb7b6dd879e29c9e2e9e0c6f9b84ae0dbdbade43a1eee3e6850d749ec1b67c42a061095")
SESSION_SECRET = binascii.unhexlify(
    b"c77a1ef7e21ba78a9b04ae1951ba594fc0fbf53c1d33dff45f689779eac7a8a759ff05c97290d9f9b04979f2d0992984c2e78d8ac7b936e5934e71826e8af833")
# 원래는 세션 별로 생성해주어야함
FORM_ID = 'example-login-form'
# 요청하는 폼 아이디
WINDOW = (datetime.timedelta(minutes=-90), datetime.timedelta(hours=36))
# ! csrf 토큰 요청 시작 시간

class _CSRF():
  @staticmethod
  def generateToken(unique_id):
    utctime = datetime.datetime.now(datetime.timezone.utc)
    return csrf.generate(SERVER_SECRET, SESSION_SECRET, unique_id, utctime)

  @staticmethod
  def validateToken(token, unique_id):
    utctime = datetime.datetime.now(datetime.timezone.utc)
    if not csrf.valid(SERVER_SECRET, SESSION_SECRET, unique_id, WINDOW, utctime + datetime.timedelta(minutes=10), token):
      return False
    return True

# ! Usage : _CSRF.generate(unique_id) / _CSRF.validate(token, unique_id)
