import binascii
import datetime
import random
import hmac

SERVER_SECRET = binascii.unhexlify(
    b"9e20abdbf8b24c91851170f2f0efebd64d732d86920bf0e2952fb18a6bb7b6dd879e29c9e2e9e0c6f9b84ae0dbdbade43a1eee3e6850d749ec1b67c42a061095")

class _CSRF():
  @classmethod
  def generateToken(cls, unique_id):
    message = f"{unique_id}:{SERVER_SECRET}"
    return hmac.new(message.encode(), digestmod='sha256').hexdigest()

  @classmethod
  def validateToken(cls, token, unique_id):
    utcnow = datetime.datetime.now(datetime.timezone.utc)
    if not cls.generateToken(unique_id) == token:
      return False
    return True

