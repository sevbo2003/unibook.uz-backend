from rest_framework.viewsets import ModelViewSet
from apps.accounts.serializers import UserSerializer
from apps.accounts.models import User
from apps.accounts.pagination import CustomPagination


class UserViewSet(ModelViewSet):
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    http_method_names = ['get', 'head', 'options']
    pagination_class = CustomPagination