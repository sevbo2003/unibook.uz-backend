from rest_framework import serializers
from apps.accounts.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'reputation', 'bio', 'joined', 'last_activity', 'avatar_url')