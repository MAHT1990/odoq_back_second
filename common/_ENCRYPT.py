from pbkdf2 import crypt
import os
import bcrypt


class ENCRYPT():
  @staticmethod
  def encrypt(raw_text):
    salt = bcrypt.gensalt().decode('ascii').replace('$', '0')
    return crypt(raw_text, salt, 1000)
  
  @staticmethod
  def validate(raw_text, target_hash):
    return (crypt(raw_text, target_hash, 1000) == target_hash)
