from django.contrib.auth import authenticate, logout
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from apps.authentication.serializers import RegisterSerializer


class RegisterView(APIView):
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class LogoutView(APIView):
    def post(self, request):
        logout(request)
        return Response({"msg": "Successfully Logged out"}, status=status.HTTP_200_OK)
