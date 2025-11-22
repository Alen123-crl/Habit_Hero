from rest_framework import serializers
from django.contrib.auth import authenticate
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError
from django.core.exceptions import ValidationError

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
class RefreshTokenSerializer(serializers.Serializer):
    refresh = serializers.CharField()

    def validate(self, data):
        refresh_token = data.get("refresh")

        try:
            refresh = RefreshToken(refresh_token)
            access_token = refresh.access_token
            
            return {
                "access": str(access_token),
                "refresh": str(refresh),
            }
        except TokenError as e:
            raise ValidationError({"refresh": "Invalid or expired refresh token."})
        except Exception as e:
            raise ValidationError({"refresh": "Invalid token format."})