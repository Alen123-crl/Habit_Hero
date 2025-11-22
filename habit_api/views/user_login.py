from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from rest_framework import status
from ..serializers.user_login import LoginSerializer,RefreshTokenSerializer

User = get_user_model()

class LoginView(APIView):

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        user = User.objects.get(id=data["user_id"])
        profile = user.profile

        profile_pic_url = (
            request.build_absolute_uri(profile.pro_pic.url)
            if profile.pro_pic else None
        )

        return Response({
            "user": {
                "id": user.id,
                "email": user.email,
                "first_name": profile.first_name,
                "last_name": profile.last_name,
                "age": profile.age,
                "profile_pic": profile_pic_url,
            },
            "tokens": {
                "access": data["access"],
                "refresh": data["refresh"],
            }
        }, status=status.HTTP_200_OK)
class RefreshTokenView(APIView):

    def post(self, request):
        serializer = RefreshTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        return Response({
            "tokens": {
                "access": data["access"],
                "refresh": data["refresh"],
            }
        }, status=status.HTTP_200_OK)