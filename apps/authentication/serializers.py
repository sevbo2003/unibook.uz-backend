from rest_framework import serializers
from apps.accounts.models import User
from apps.authentication.validators import validate_user


class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("username", "email", "password")
        extra_kwargs = {"username": {"validators": [validate_user]}}

    def create(self, validated_data):
        user = User(username=validated_data["username"], email=validated_data["email"])
        password = validated_data["password"]
        user.set_password(password)
        user.save()
        return user
