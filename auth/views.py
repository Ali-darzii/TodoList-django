from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.views import APIView
from rest_framework.request import Request
from utils.utils import IsNotAuthenticated, ErrorResponses
from .serializers import UserRegisterSerializer, UserLoginSerializer
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import AccessToken, RefreshToken
from django.contrib.auth import user_logged_in
from django.utils import timezone


# Create your views here.


class AuthAPIView(APIView):
    permission_classes = (IsNotAuthenticated,)

    @action(methods=['POST'], detail=True)
    def post(self, request: Request):
        """ Register User"""
        serializer = UserRegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = User.objects.create(
            username=serializer.validated_data['email'],
            email=serializer.validated_data['email']
        )
        user.set_password(serializer.validated_data['password'])
        user.last_login = timezone.now()
        user.save()
        user_logged_in.send(sender=self.__class__, request=request, user=user)
        data = {
            "access_token": str(AccessToken.for_user(user)),
            "refresh_token": str(RefreshToken.for_user(user)),
        }
        return Response(data=data, status=status.HTTP_201_CREATED)

    @action(methods=['PUT'], detail=True)
    def put(self, request: Request):
        serializer = UserLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            user = User.objects.get(email=serializer.validated_data["email"])
        except User.DoesNotExist:
            return Response(data=ErrorResponses.USER_NOT_FOUND, status=status.HTTP_404_NOT_FOUND)

        if not user.check_password(serializer.validated_data["password"]):
            return Response(data=ErrorResponses.USER_NOT_FOUND, status=status.HTTP_404_NOT_FOUND)

        user.last_login = timezone.now()
        user.save()
        data = {
            "access_token": str(AccessToken.for_user(user)),
            "refresh_token": str(RefreshToken.for_user(user))
        }
        return Response(data=data, status=status.HTTP_200_OK)
