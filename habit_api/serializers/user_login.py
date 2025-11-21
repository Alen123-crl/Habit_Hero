from rest_framework import serializers
from django.contrib.auth import authenticate
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.tokens import RefreshToken

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):

        email = data.get("email")
        password = data.get("password")

        user = authenticate(email=email, password=password)

        if not user:
            raise AuthenticationFailed("Invalid Credentials")

        refresh = RefreshToken.for_user(user)

        return {
            "user_id": user.id,
            "refresh": str(refresh),
            "access": str(refresh.access_token),
        }
