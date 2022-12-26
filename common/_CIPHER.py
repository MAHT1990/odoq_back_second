from Cryptodome.Cipher import AES
from Cryptodome.Util.Padding import pad, unpad
from django.conf import settings
import base64


class AESCipherCBC(object):
  def __init__(self):
    self.BS = int(settings.CIPHER_IV_LENGTH)
    self.key = settings.CIPHER_KEY.encode(settings.CIPHER_INPUT_ENCODE)

  def encrypt(self, raw=settings.CIPHER_KEY):
    cipher = AES.new(self.key, AES.MODE_CBC)
    ct_bytes = cipher.encrypt(pad(raw.encode(settings.CIPHER_INPUT_ENCODE), self.BS))
    iv = base64.b64encode(cipher.iv).decode(settings.CIPHER_INPUT_ENCODE)
    ct = base64.b64encode(ct_bytes).decode(settings.CIPHER_INPUT_ENCODE)

    return f'{iv}:{ct}'

  def decrypt(self, enc):
    enc_arr = enc.split(':')
    if len(enc_arr) != 2:
      return None

    iv = base64.b64decode(enc_arr[0].encode(settings.CIPHER_INPUT_ENCODE))
    ct = base64.b64decode(enc_arr[1].encode(settings.CIPHER_INPUT_ENCODE))
    cipher = AES.new(self.key, AES.MODE_CBC, iv=iv)

    return unpad(cipher.decrypt(ct), self.BS)

