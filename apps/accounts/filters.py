from django_filters import rest_framework as filters
from apps.accounts.models import User


class UserFilter(filters.FilterSet):
    min_reputation = filters.NumberFilter(field_name='reputation', lookup_expr='gte')
    max_reputation = filters.NumberFilter(field_name='reputation', lookup_expr='lte')

    class Meta:
        model = User
        fields = ['username']