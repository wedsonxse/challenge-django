

from django.conf.urls import url
from profiles.views import UserProfileView


urlpatterns = [
    url(r'^me', UserProfileView.as_view()),
    ]