from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from ..serializers.user import UserUpdateSerializer

class UserView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        profile = getattr(user, "profile", None)
        data = {
            "email": user.email,
            "first_name": profile.first_name if profile else "",
            "last_name": profile.last_name if profile else "",
            "age": profile.age if profile else None,
            "pro_pic": request.build_absolute_uri(profile.pro_pic.url) if profile and profile.pro_pic else None,
        }
        return Response(data, status=status.HTTP_200_OK)

    def patch(self, request):
        """Partial update"""
        user = request.user
        serializer = UserUpdateSerializer(user, data=request.data,partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "User updated successfully"}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request):
        """Delete own account"""
        user = request.user
        user.delete()
        return Response({"message": "User deleted successfully"}, status=status.HTTP_200_OK)
