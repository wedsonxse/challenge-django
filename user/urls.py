

from django.conf.urls import url
from user.views import UserRegistrationView
from user.views import UserLoginView 

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    url(r'^signup', UserRegistrationView.as_view()),
    url(r'^signin', UserLoginView.as_view()),

    ]