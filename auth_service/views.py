from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.views import APIView
from rest_framework.request import Request
from utils.utils import IsNotAuthenticated, ErrorResponses, DocumentProperties
from .serializers import UserRegisterSerializer, UserLoginSerializer
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import AccessToken, RefreshToken
from django.contrib.auth import user_logged_in, user_login_failed
from django.utils import timezone
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi


class AuthAPIView(APIView):
    permission_classes = (IsNotAuthenticated,)

    @swagger_auto_schema(
        method='POST',
        operation_id='user_signup',
        operation_description='creating user, client must not have any Authorize)',
        responses={201: openapi.Response(description='returning JWT',
                                         schema=openapi.Schema(
                                             type=openapi.TYPE_OBJECT, properties=DocumentProperties.authResponses),

                                         )},
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['email', 'password'],
            properties=DocumentProperties.authProperties
        )
    )
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

    @swagger_auto_schema(
        method='PUT',
        operation_id='user_login',
        operation_description='login user, client must not have any Authorize',
        responses={200: openapi.Response(description='returning JWT',
                                         schema=openapi.Schema(
                                             type=openapi.TYPE_OBJECT, properties=DocumentProperties.authResponses),
                                         )},
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['email', 'password'],
            properties=DocumentProperties.authProperties
        )
    )
    @action(methods=['PUT'], detail=True)
    def put(self, request: Request):
        serializer = UserLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            user = User.objects.get(email=serializer.validated_data["email"])
        except User.DoesNotExist:
            return Response(data=ErrorResponses.USER_NOT_FOUND, status=status.HTTP_404_NOT_FOUND)

        if not user.check_password(serializer.validated_data["password"]):
            user_login_failed.send(sender=self.__class__, request=request, user=user)
            return Response(data=ErrorResponses.USER_NOT_FOUND, status=status.HTTP_404_NOT_FOUND)

        user.last_login = timezone.now()
        user.save()
        data = {
            "access_token": str(AccessToken.for_user(user)),
            "refresh_token": str(RefreshToken.for_user(user))
        }
        return Response(data=data, status=status.HTTP_200_OK)


class UserAPI(APIView):
    permission_classes = (IsAuthenticated,)

    @swagger_auto_schema(
        method='DELETE',
        operation_id='user_remove',
        operation_description='user remove, client must be authenticated',
        responses={204: openapi.Response(description='returning no content', )},
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['refresh_token'],
            properties=DocumentProperties.userRemoveProperties
        )
    )
    @action(methods=["delete"], detail=True)
    def delete(self, request: Request):
        """ delete user """
        try:
            refresh_token = request.data["refresh_token"]
            tk = RefreshToken(refresh_token)
            tk.blacklist()
        except Exception:
            return Response(ErrorResponses.TOKEN_IS_EXPIRED_OR_INVALID, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = User.objects.get(pk=request.user.id)
            user.delete()
            return Response(data={'message': "Successfully user deleted."}, status=status.HTTP_204_NO_CONTENT)
        except User.DoesNotExist:
            return Response(data=ErrorResponses.USER_NOT_FOUND, status=status.HTTP_404_NOT_FOUND)

    @swagger_auto_schema(
        method='POST',
        operation_id='user_logout',
        operation_description='user logout, client must be authenticated',
        responses={204: openapi.Response(description='returning no content', )},
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['refresh_token'],
            properties=DocumentProperties.userRemoveProperties
        )
    )
    @action(detail=True, methods=['post'])
    def post(self, request):
        """ user logout """
        try:
            refresh_token = request.data["refresh_token"]
            tk = RefreshToken(refresh_token)
            tk.blacklist()
            return Response(data={'message': "Successfully logged out."}, status=status.HTTP_204_NO_CONTENT)
        except Exception:
            return Response(ErrorResponses.TOKEN_IS_EXPIRED_OR_INVALID, status=status.HTTP_400_BAD_REQUEST)
