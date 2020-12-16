from django.shortcuts import render
from rest_framework import status
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from user.serializers import UserRegistrationSerializer
from rest_framework.generics import RetrieveAPIView
from user.serializers import UserLoginSerializer
from user.models import User

from django.contrib.auth.models import update_last_login
from rest_framework import serializers
from rest_framework_jwt.settings import api_settings

JWT_PAYLOAD_HANDLER = api_settings.JWT_PAYLOAD_HANDLER
JWT_ENCODE_HANDLER = api_settings.JWT_ENCODE_HANDLER

class UserRegistrationView(CreateAPIView):

    serializer_class = UserRegistrationSerializer
    permission_classes = (AllowAny,)

    def post(self, request):

        
        data = {'e_mail':request.data['e_mail'],'password':request.data['password'],
                'profile':{'first_name':request.data['first_name'], 'last_name':request.data['last_name'],'phone_number':request.data['phone'],
                 'area_code':request.data['area_code'], 'country_code':request.data['country_code'] }}

        print('TESTANDO:' + str(data))

        serializer = self.serializer_class(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        u = User.objects.get(e_mail = data['e_mail'])

        try:
            payload = JWT_PAYLOAD_HANDLER(u)
            jwt_token = JWT_ENCODE_HANDLER(payload)
            update_last_login(None, u)
        except User.DoesNotExist:
            raise serializers.ValidationError(
                'Invalid e-mail or password'
            )

        status_code = status.HTTP_201_CREATED

        response = {
            'success' : 'True',
            'status code' : status_code,
            'message': 'User registered successfully',
            'token' : jwt_token,
            }
        
        return Response(response, status=status_code)

class UserLoginView(RetrieveAPIView):

    permission_classes = (AllowAny,)
    serializer_class = UserLoginSerializer

    def post(self, request):

        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        response = {
            'success' : 'True',
            'status code' : status.HTTP_200_OK,
            'message': 'User logged in  successfully',
            'jwt_token' : serializer.data['token'],
            }
            
        status_code = status.HTTP_200_OK

        return Response(response, status=status_code)
