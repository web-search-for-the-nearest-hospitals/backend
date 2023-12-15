from django.conf import settings
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from rest_framework import filters, permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from api.permissions import IsAdmin
from user.models import User
from user.serializers import AuthSerializer, TokenSerializer, UserSerializer


class UserViewSet(viewsets.ModelViewSet):
    filter_backends = (filters.SearchFilter,)
    http_method_names = ["get", "post", "patch", "delete"]
    lookup_field = "username"
    permission_classes = (
        permissions.IsAuthenticated,
        IsAdmin,
    )
    queryset = User.objects.all()
    search_fields = ("username",)
    serializer_class = UserSerializer

    @action(
        methods=["GET", "PATCH"],
        detail=False,
        permission_classes=(permissions.IsAuthenticated,),
    )
    def me(self, request):
        if request.method == "GET":
            return Response(
                UserSerializer(request.user).data,
                status=status.HTTP_200_OK,
            )

        serializer = UserSerializer(
            request.user,
            data=request.data,
            partial=True,
        )
        serializer.is_valid(raise_exception=True)
        serializer.save(role=request.user.role)
        return Response(serializer.data, status=status.HTTP_200_OK)


class AuthView(APIView):
    def make_token(self, user):
        return default_token_generator.make_token(user)

    def send_token(self, user, username, email):
        send_mail(
            "код подтверждения",
            self.make_token(user),
            settings.DEFAULT_FROM_EMAIL,
            (email,),
        )

    def post(self, request):
        serializer = AuthSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        username = serializer.validated_data["username"]
        email = serializer.validated_data["email"]
        try:
            user, created = User.objects.get_or_create(
                username=username,
                email=email,
            )
        except Exception:
            raise ValidationError
        self.send_token(user, username, email)
        return Response(
            {"username": username, "email": email},
            status=status.HTTP_200_OK,
        )


class UserTokenView(APIView):
    def post(self, request):
        serializer = TokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        username = serializer.validated_data["username"]
        user = get_object_or_404(User, username=username)
        confirmation_code = serializer.validated_data.get("confirmation_code")
        if not default_token_generator.check_token(user, confirmation_code):
            return Response(
                {"Вы использовали неверный код подтверждения."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        token = RefreshToken.for_user(user)
        return Response(
            {"token": str(token.access_token)},
            status=status.HTTP_200_OK,
        )
