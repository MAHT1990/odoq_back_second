import mysqlmodel.models as mysqlModels
from utils import common

class _CODE():
  def __init__(self, code_group):
    retrievedDict = mysqlModels.CommonCode.objects.filter(code_group=code_group)
    self.commonDict = common.make_dictionary(retrievedDict ,'code', 'name')
    self.commonNameDict = common.make_dictionary(retrievedDict, 'name', 'code')
  
  def GET_NAME_WITH_CODE(self, code):
    return (self.commonDict[code]) or ''
  
  def GET_CODE_WITH_NAME(self, name):
    return (self.commonNameDict[name]) or ''
