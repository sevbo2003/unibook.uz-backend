from rest_framework.viewsets import ModelViewSet
from apps.accounts.serializers import UserSerializer
from apps.accounts.models import User


class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    http_method_names = ['get', 'head', 'options']