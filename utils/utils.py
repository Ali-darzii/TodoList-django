from rest_framework import status, serializers
from rest_framework.exceptions import APIException
from rest_framework.request import Request
from rest_framework.permissions import BasePermission, SAFE_METHODS
import re


def get_client_ip(request: Request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


class ErrorResponses:
    SOMETHING_WENT_WRONG = {'detail': "WE_ALSO_DON'T_KNOW_WHAT_HAPPENED!", 'error_code': 1}
    ALREADY_TAKEN = {'detail': 'ALREADY_TAKEN', 'error_code': 2}
    TOKEN_IS_EXPIRED_OR_INVALID = ""
    TARGET_USER_NOT_FOUND = {'detail': 'TARGET_USER_NOT_FOUND', 'error_code': 4}
    BAD_FORMAT = {'detail': 'BAD_FORMAT', 'error_code': 5}
    USER_NOT_FOUND = {'detail': 'USER_NOT_FOUND', 'error_code': 6}
    OBJECT_NOT_FOUND = {'detail': 'OBJECT_NOT_FOUND', 'error_code': 7}


class NotAuthorized(APIException):
    status_code = status.HTTP_403_FORBIDDEN
    default_detail = "Authenticated users are not allowed to access to get jwt."
    default_code = "not_authorized"


class IsNotAuthenticated(BasePermission):
    def has_permission(self, request, view):
        aa = request.META.get("Authorization", None)
        print("Here is : ",aa)
        if 'HTTP_AUTHORIZATION' in request.META and request.META['HTTP_AUTHORIZATION']:
            raise NotAuthorized()
        return not request.user.is_authenticated


def validate_password(password: str):
    """
             3 parameters:
             1- 8 character >=
             2- numeric and character
             3- use 1 sign character
             """
    symbols = r'[!@#$%^&*()\[\]{}|\\/:;"\'<>,.?]'
    message = {"check": True}
    if len(password) >= 8:
        if re.search('[1-9]', password) and re.search('[a-z]', password):
            if re.search(symbols, password):
                return message
            else:
                message["check"] = False
                message["detail"] = "must contain at least 1 symbol"

        else:
            message["check"] = False
            message["detail"] = "must contain numeric and character"
    else:
        message["check"] = False
        message["detail"] = "must contain 8 character or more"

    return message
