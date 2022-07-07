from rest_framework import serializers
from apps.accounts.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'reputation', 'bio', 'joined', 'last_activity', 'avatar_url', 'avatar')
        read_only_fields = ('id', 'username', 'reputation', 'joined', 'last_activity', 'avatar_url')
        extra_kwargs = {
            'avatar': {'write_only': True},
        }
        
    def update(self, instance, validated_data):
        instance.username = validated_data.get("username", instance.username)
        instance.bio = validated_data.get("bio", instance.bio)
        instance.avatar = validated_data.get("avatar", instance.avatar)
        instance.save()
        return instance