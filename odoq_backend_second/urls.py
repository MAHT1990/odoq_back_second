"""odoq_backend_second URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls.static import static
from django.conf import settings
from django.contrib import admin
from django.urls import path
import api

urlpatterns = [
    path('admin/', admin.site.urls),
]

urlpatterns_csrf = [
    path('api/csrf/', api.csrf.views.TokenViewSet.as_view()),
]

urlpatterns_user = [
    path('api/user/', api.user.views.index),
    path('api/user/accept_sms/', api.user.accept_sms.views.AcceptSMS.as_view()),
    path('api/user/login/', api.user.login.views.LoginUserModel.as_view()),
    path('api/user/signup/', api.user.login.views.index),
    path('api/user/signup/send_sms_auth/', api.user.signup.views.SendSMSAuth.as_view()),
    path('api/user/signup/verify_sms_auth/', api.user.signup.views.VerifySMSAuth.as_view()),
    path('api/user/signup/create/', api.user.signup.views.RegistUser.as_view()),
]

urlpatterns_notice = [
    path('api/notice/', api.notice.views.NoticeView.as_view()),
]

urlpatterns_question = [
    path('api/question/', api.question.views.QuestionView.as_view()),
    path('api/question/answer_history/', api.question.views.AnswerHistoryView.as_view()),
]

urlpatterns_post = [
    path('api/post/', api.post.views.PostView.as_view()),
]

urlpatterns_sms = [
    path('api/sms/', api.sms.views.SMSView.as_view()),
]

urlpatterns += urlpatterns_csrf
urlpatterns += urlpatterns_user
urlpatterns += urlpatterns_question
urlpatterns += urlpatterns_post
urlpatterns += urlpatterns_sms
urlpatterns += urlpatterns_notice

# Media
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)