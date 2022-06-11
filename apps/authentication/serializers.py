from rest_framework import serializers
from apps.accounts.models import User


class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("username", "email", "password", "bio", "avatar")

    def create(self, validated_data):
        user = User(username=validated_data["username"], email=validated_data["email"])
        password = validated_data["password"]
        user.set_password(password)
        user.save()
        return user

    def update(self, instance, validated_data):
        instance.username = validated_data.get("username", instance.username)
        instance.bio = validated_data.get("bio", instance.bio)
        instance.avatar = validated_data.get("avatar", instance.avatar)
        password = validated_data["password"]
        instance.set_password(password)
        instance.save()
        return instance
