

from django.conf.urls import url
from user.views import UserRegistrationView
from user.views import UserLoginView

urlpatterns = [
    url('signup', UserRegistrationView.as_view()),
    url('signin', UserLoginView.as_view()),

    ]