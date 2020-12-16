
from rest_framework import status
from rest_framework.generics import RetrieveAPIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from user.models import User
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from user.serializers import UserRegistrationSerializer
from profiles.models import UserProfile


class UserProfileView(RetrieveAPIView):

    permission_classes = (IsAuthenticated,)
    authentication_class = JSONWebTokenAuthentication

    def get(self, request):
        print('valor da requisição:    ' + str(request.user))
        try:
            user_profile = UserProfile.objects.get(user=request.user)

            u = User.objects.get(e_mail = request.user)
            last = u.last_login
            create = u.date_joined

            status_code = status.HTTP_200_OK
            response = {
                'message' : 'User profile fetched successfully',
                'status code': status_code,
                'user info': [{
                    'first_name': user_profile.first_name,
                    'last_name': user_profile.last_name,
                    'phone_number': user_profile.phone_number,
                    'area_code': user_profile.area_code,
                    'country_code': user_profile.country_code,
                    'last login':last,
                    'created_at':create
                    }]
                }

        except Exception as e:
            status_code = status.HTTP_400_BAD_REQUEST
            response = {
                'message' : 'User does not exists',
                'status code': status.HTTP_400_BAD_REQUEST,
                'error': str(e)
            }

        return Response(response, status=status_code)