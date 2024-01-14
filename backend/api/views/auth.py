from rest_framework import status
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from django.middleware import csrf

from backend import settings
from ..serializers import SignUpSerializer, TokenSerializer
from user.models import User


def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }


class SignUp(APIView):
    """Вью для регистрации нового пользователя"""
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = SignUpSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        # username = serializer.data.get('username')
        email = serializer.data.get('email')
        user, _ = User.objects.get_or_create(
            **serializer.validated_data
        )
        return Response(
            serializer.data,
            status=status.HTTP_200_OK
        )


class LoginView(APIView):
    def post(self, request, format=None):
        serializer = TokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = request.data
        response = Response()
        email = data.get('email', None)
        password = data.get('password', None)
        user = get_object_or_404(
            User, email=email, password=password
        )
        if user is not None:
            if user.is_active:
                data = get_tokens_for_user(user)
                response.set_cookie(
                    key=settings.SIMPLE_JWT['AUTH_COOKIE'],
                    value=data["refresh"],
                    expires=settings.SIMPLE_JWT['ACCESS_TOKEN_LIFETIME'],
                    secure=settings.SIMPLE_JWT['AUTH_COOKIE_SECURE'],
                    httponly=settings.SIMPLE_JWT['AUTH_COOKIE_HTTP_ONLY'],
                    samesite=settings.SIMPLE_JWT['AUTH_COOKIE_SAMESITE'],
                )
                csrf.get_token(request)
                response.data = {"Success": "Аутентификация пройдена", "data": data}

                return response
            else:
                return Response({"No active": "Аккаунт неактивен!"}, status=status.HTTP_404_NOT_FOUND)
        else:
            return Response({"Invalid": "Неверное имя пользователя или пароль!"}, status=status.HTTP_404_NOT_FOUND)
