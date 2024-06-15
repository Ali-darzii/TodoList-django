from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from rest_framework import serializers
from django.contrib.auth.models import User
from utils.utils import validate_password
from utils.utils import ErrorResponses


class UserRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("password", "email")

    def validate_email(self, email):
        """ Validate email and username exist check """
        try:
            validate_email(email)
            return email
        except ValidationError:
            raise serializers.ValidationError(detail=ErrorResponses.BAD_FORMAT)

    def validate_password(self, password):
        password_validation = validate_password(password)
        if not password_validation["check"]:
            raise serializers.ValidationError(detail=password_validation["detail"])
        return password


class UserLoginSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ("password", "email",)

    def validate_email(self, email):
        try:
            validate_email(email)
            return email
        except ValidationError:
            raise serializers.ValidationError(detail=ErrorResponses.BAD_FORMAT)

    def validate_password(self, password):
        password_validation = validate_password(password)
        if not password_validation["check"]:
            raise serializers.ValidationError(detail=password_validation["detail"])
        return password
