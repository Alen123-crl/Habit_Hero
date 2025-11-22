from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from ..serializers.user_signup import UserSignUpSerializer
from django.contrib.auth import get_user_model

User = get_user_model()


class UserSignUpView(APIView):

    permission_classes = []
    authentication_classes = []

    def post(self, request):
        serializer = UserSignUpSerializer(data=request.data)

        if serializer.is_valid():
            user = serializer.save()

            return Response(
                {
                    "message": "User registered successfully",
                },
                status=status.HTTP_201_CREATED,
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)