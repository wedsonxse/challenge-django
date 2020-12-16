

from django.conf.urls import url
from profiles.views import UserProfileView


urlpatterns = [
    url('me', UserProfileView.as_view()),
    ]