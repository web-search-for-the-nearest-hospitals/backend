from django.conf import settings
from django.contrib.auth import authenticate
from django.contrib.auth.tokens import default_token_generator
from django.middleware import csrf
from django.utils.decorators import method_decorator
from djoser import utils
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from templated_mail.mail import BaseEmailMessage

from .models import User
from .schemas import SIGNUP_SCHEMAS, LOGIN_SCHEMAS
from .serializers import SignUpSerializer, TokenSerializer


def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }


@method_decorator(
    name="post",
    decorator=swagger_auto_schema(
        tags=SIGNUP_SCHEMAS["post"]["tags"],
        operation_summary=SIGNUP_SCHEMAS["post"]["summary"],
        operation_description=SIGNUP_SCHEMAS["post"]["description"],
        responses=SIGNUP_SCHEMAS["post"]["responses"],
        security=[]
    )
)
class SignUp(APIView):
    """Вью для регистрации нового пользователя"""
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = SignUpSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user, _ = User.objects.get_or_create(
            **serializer.validated_data
        )
        return Response(
            status=status.HTTP_201_CREATED
        )


@method_decorator(
    name="post",
    decorator=swagger_auto_schema(
        tags=LOGIN_SCHEMAS["post"]["tags"],
        operation_summary=LOGIN_SCHEMAS["post"]["summary"],
        operation_description=LOGIN_SCHEMAS["post"]["description"],
        responses=LOGIN_SCHEMAS["post"]["responses"],
        security=[]
    )
)
class LoginView(APIView):
    """Вью для авторизации зарегистрированного пользователя"""

    def post(self, request, format=None):
        serializer = TokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = request.data
        response = Response()
        email = data.get('email')
        password = data.get('password')
        user = authenticate(email=email, password=password)
        if user:
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
            response.data = {"Success": "Аутентификация пройдена",
                             "data": data}
            return response
        return Response({
            "Invalid": "Неверное имя пользователя или пароль!"
        }, status=status.HTTP_400_BAD_REQUEST)


class PasswordResetEmail(BaseEmailMessage):
    """Переопределяем класс джосера для отправки письма."""
    template_name = "password_reset.html"

    def get_context_data(self):
        from djoser.conf import settings
        # PasswordResetEmail can be deleted
        context = super().get_context_data()

        user = context.get("user")
        context["uid"] = utils.encode_uid(user.pk)
        context["token"] = default_token_generator.make_token(user)
        context["url"] = settings.PASSWORD_RESET_CONFIRM_URL.format(**context)
        return context
