from django.shortcuts import render

# Create your views here.

from django.contrib.auth import authenticate
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status, generics, filters
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import *

from sixbox_user.models import S_User
from sixbox_user.serializers import User_Register_Serializer, User_Login_Serializer, User_Serializer


class RegisterAPIView(APIView):
    permission_classes = (AllowAny,)

    @swagger_auto_schema(request_body=User_Register_Serializer)
    def post(self, request, *args, **kwargs):
        serializer = User_Register_Serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(data={
            'message': 'good',
            'status': 'CREATED'
        }, status=status.HTTP_201_CREATED)


class LoginAPIView(APIView):
    permission_classes = (AllowAny,)

    @swagger_auto_schema(request_body=User_Login_Serializer)
    def post(self, request):
        serializer = User_Login_Serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = authenticate(username=serializer.validated_data['username'],
                            email=serializer.validated_data['email'],
                            password=serializer.validated_data['password'])
        if not user:
            return Response(status=status.HTTP_404_NOT_FOUND,
                            data={'message': 'User not found or does not exist'})
        else:
            token = Token.objects.get_or_create(user=user)
            return Response(data={'token': str(token)},
                            status=status.HTTP_200_OK)


class UserSearchView(generics.ListAPIView):
    queryset = S_User.objects.all()
    serializer_class = User_Serializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['username', 'number']
