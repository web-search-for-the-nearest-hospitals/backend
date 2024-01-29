import re

from django.contrib.auth.hashers import make_password
from django.core.exceptions import ValidationError
from djoser import utils
from djoser.conf import settings
from djoser.serializers import PasswordRetypeSerializer
from rest_framework import serializers

from .models import User


class SignUpSerializer(serializers.Serializer):
    """Сериализатор регистрации нового пользователя."""

    regex_for_password = r'[a-zA-Z0-9]{8,}'
    email = serializers.EmailField(
        max_length=254,
        required=True,
    )
    # пока заглушка в виде не менее 8 букв или цифр
    password = serializers.RegexField(
        regex_for_password,
        required=True,
    )

    def validate(self, data):
        email = data.get('email')
        password = data.get('password')
        hashed_password = make_password(password)
        data['password'] = hashed_password
        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError(
                'Пользователь с такой почтой уже существует!'
            )
        return data


class TokenSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(required=True)


class UidAndTokenSerializer(serializers.Serializer):
    """Сериализатор проверки текущего пользователя."""
    uid = serializers.CharField(required=False)
    token = serializers.CharField(required=False)

    default_error_messages = {
        "invalid_token": settings.CONSTANTS.messages.INVALID_TOKEN_ERROR,
        "invalid_uid": settings.CONSTANTS.messages.INVALID_UID_ERROR,
    }

    def custom_validator(self):
        request_object = self.context['request']
        url = request_object._request.path
        find_uid = re.search(
            r'(?<=\/reset_password_confirm\/)([A-Za-z]{3})', url)
        uid = find_uid.group()
        find_token = re.search(
            r'(?<=\/reset_password_confirm\/[A-Za-z]{3}\/)([\w-]+)', url)
        token = find_token.group()
        return {
            "uid": uid,
            "token": token
        }

    def validate(self, attrs):
        self.custom_validator()
        uid = self.custom_validator().get('uid')
        try:
            uid = utils.decode_uid(uid)
            self.user = User.objects.get(pk=uid)
        except (User.DoesNotExist, ValueError, TypeError, OverflowError):
            key_error = "invalid_uid"
            raise ValidationError(
                {"uid": [self.error_messages[key_error]]}, code=key_error
            )
        return super().validate(attrs)


class PasswordResetConfirmRetypeSerializer(UidAndTokenSerializer,
                                           PasswordRetypeSerializer):
    """PasswordRetypeSerializer взят из джосера,
    UidAndTokenSerializer переопределен.
    """
    pass
