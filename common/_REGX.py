import re


class Regex(object):
  def __init__(self, pattern_type, string):
    self.pattern_type = pattern_type
    self.string = string

  def match(self):
    if not self.string:
      return {'success': False, 'message': '매칭시킬 string이 존재하지 않습니다.'}

    pattern = self.__get_pattern_dict().get(self.pattern_type, None)

    if pattern is None:
      return {'success': False, 'message': '매칭되는 정규식이 존재하지 않습니다.'}

    regex = re.compile(pattern, re.IGNORECASE)
    return {'success': True, 'message': None, 'is_matched': (re.match(regex, self.string) is not None)}

# define regex pattern dictionary
  def __get_pattern_dict(self):
    return {
      'url': (
        r'^(?:http|ftp)s?://' # http:// or https://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|' #domain...
        r'localhost|' #localhost...
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})' # ...or ip
        r'(?::\d+)?' # optional port
        r'(?:/?|[/?]\S+)$'
      )
    }