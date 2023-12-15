from rest_framework import serializers


from user.models import User


class AuthSerializer(serializers.Serializer):
    username = serializers.SlugField(max_length=150)
    email = serializers.EmailField(max_length=254, required=True)

    class Meta:
        model = User
        fields = ("email", "username")


class TokenSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150)
    confirmation_code = serializers.CharField(max_length=150)


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "username",
            "email",
            "role",
            "first_name",
            "last_name",
            "phone",
            "date_of_birth",
        )
