from django.contrib.auth import authenticate, logout
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from apps.authentication.serializers import RegisterSerializer
from apps.authentication.utils import get_token_for_user


class RegisterView(APIView):
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class LoginView(APIView):
    def post(self, request):
        if "username" not in request.data or "password" not in request.data:
            return Response({"msg": "Credentials missing"}, status=status.HTTP_400_BAD_REQUEST)
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            auth_data = get_token_for_user(request.user)
            return Response({"msg": "Login Success", **auth_data}, status=status.HTTP_200_OK)
        return Response({"msg": "Invalid Credentials"}, status=status.HTTP_401_UNAUTHORIZED)


class LogoutView(APIView):
    def post(self, request):
        logout(request)
        return Response({"msg": "Successfully Logged out"}, status=status.HTTP_200_OK)
