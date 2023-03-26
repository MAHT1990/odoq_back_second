import odoq_models.models as OdoqModels

class GetAcceptSMS:
    def __init__(self, request):
        self.request = request
        self.user_id = request.GET.get('userId', None)

    def make_data(self):
        print('## api/user/accept_sms/services.py > GetAcceptSMS self.user_id is ', self.user_id, type(self.user_id))
        if self.user_id is not None and self.user_id != '0':
            user = OdoqModels.User.objects.get(id=self.user_id)
            data = {
                'accept_sms': user.accept_sms,
            }
        else:
            data = {
                'accept_sms': False,
            }
        return data

class CheckAcceptSMS:
    def __init__(self, request):
        self.request = request
        self.user_id = request.data.get('userId', None)

    def make_data(self):
        print('## api/user/accept_sms/services.py > CheckAcceptSMS self.user_id is ', self.user_id, type(self.user_id))
        if self.user_id is not None:
            user = OdoqModels.User.objects.get(id=self.user_id)
            user.accept_sms = not user.accept_sms
            user.save()
            data = {
                'accept_sms': user.accept_sms,
            }
        else:
            data = {
                'accept_sms': False,
            }
        return data