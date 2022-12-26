import requests
import json
from ._REGX import Regex
from ._CIPHER import AESCipherCBC


class WebRequest(object):
  def __init__(self, method_name, url, dict_data, is_urlencoded=False, use_cipher=False, version=None, iamport_token=None):
    self.method_name = method_name.upper()
    self.url = url
    self.dict_data = dict_data
    self.is_urlencoded = is_urlencoded
    self.use_cipher = use_cipher
    self.version = version
    self.iamport_token = iamport_token

  def __call__(self):
    response = None

    if not self.url:
      return {'success': False, 'message': 'URL이 존재하지 않습니다.'}

    result_url = Regex('url', self.url).match()
    if not result_url['success']:
      return {'success': False, 'message': f'URL: {result_url["message"]}'}
    elif not result_url['is_matched']:
      return {'success': False, 'message': 'URL 유효성이 맞지 않습니다.'}

    if self.method_name not in ('GET', 'POST'):
      return {'success': False, 'message': 'method_name은 GET/POST만 가능합니다.'}

    if self.method_name == 'GET':
      response = requests.get(url=self.url, params=self.dict_data, headers=self.__get_headers(), verify=self.__verify())
    elif self.method_name == 'POST':
      response = requests.post(url=self.url, data=self.__get_data(), headers=self.__get_headers(), verify=self.__verify())

    dict_meta = {
      'ok': response.ok,
      'status_code': response.status_code,
      'encoding': response.encoding,
      'Content-Type': response.headers['Content-Type']
    }

    return {'success': True, 'message': None, 'result': self.__get_result(response, dict_meta)}
    # return {'success': True}

  def __get_headers(self):
    if self.is_urlencoded:
      content_type = 'application/x-www-form-urlencoded'
    else:
      if self.version:
        content_type = f'application/json;version={self.version}'
      else:
        content_type = 'application/json;'

    headers = {
      'Content-Type': content_type,
    }

    if self.use_cipher:
      headers['X-ENCRYPT-DATA'] = AESCipherCBC().encrypt()

    if self.iamport_token:
      headers['Authorization'] = f'Bearer {self.iamport_token}'

    return headers

  def __get_data(self):
    if self.is_urlencoded:
      return self.dict_data
    else:
      return json.dumps(self.dict_data)

  def __get_result(self, response, dict_meta):
    if 'json' in str(response.headers['Content-Type']):  # JSON 형태인 경우
      resp_json = response.json()
      if type(resp_json) is list:
        return {**dict_meta, **{'list_data': resp_json}}
      else:
        return {**dict_meta, **resp_json}
    else:  # 문자열 형태인 경우
      return {**dict_meta, **{'text': response.text}}

  def __verify(self):
    return 'http' in self.url

