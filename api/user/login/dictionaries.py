class GetDataTable():
  def __init__(self, token):
    self.token = token
    self.data = {}

  def make_data(self):
    self.data['token'] = self.token

    return self.data