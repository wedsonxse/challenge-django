
from profiles.models import UserProfile
from user.models import User
from django.contrib.auth import authenticate
from django.contrib.auth.models import update_last_login
from rest_framework import serializers
from rest_framework import status

from rest_framework_jwt.settings import api_settings

JWT_PAYLOAD_HANDLER = api_settings.JWT_PAYLOAD_HANDLER
JWT_ENCODE_HANDLER = api_settings.JWT_ENCODE_HANDLER

class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserProfile
        fields = ('first_name', 'last_name', 'phone_number', 'area_code', 'country_code')


class UserRegistrationSerializer(serializers.ModelSerializer):

    profile = UserSerializer(required=False)

    class Meta:
        model = User
        fields = ('e_mail', 'password', 'profile')
        extra_kwargs = {'password': {'write_only': True}}
    
    def create(self, validated_data):
        profile_data = validated_data.pop('profile')
        user = User.objects.create_user(**validated_data)
        user.set_password(validated_data['password'])
        UserProfile.objects.create(
            user=user,
            first_name=profile_data['first_name'],
            last_name=profile_data['last_name'],
            phone_number=profile_data['phone_number'],
            area_code=profile_data['area_code'],
            country_code=profile_data['country_code']
        )

        return user

class UserLoginSerializer(serializers.Serializer):

    e_mail = serializers.EmailField(max_length=255)
    password = serializers.CharField(max_length=128, write_only=True)
    token = serializers.CharField(max_length=255, read_only=True)

    def validate(self, data):
        e_mail = data.get("e_mail",None)
        password = data.get("password",None)

        user = authenticate(e_mail=e_mail, password = password)
        
        status_code = status.HTTP_400_BAD_REQUEST

        if user is None:
            raise serializers.ValidationError({
                'message':'A user with this email and password is not found.',
                'error Code': status_code
            })

        try:
            payload = JWT_PAYLOAD_HANDLER(user)
            jwt_token = JWT_ENCODE_HANDLER(payload)
            update_last_login(None, user)
        except User.DoesNotExist:
            raise serializers.ValidationError(
                'User with given email and password does not exists'
            )

        return {
            "e_mail":user.e_mail,
            "token" : jwt_token
        }
        