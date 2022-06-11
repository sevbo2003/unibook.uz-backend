from datetime import timedelta as td
from django.utils import timezone
from django.conf import settings
from dateutil.parser import parse

from apps.accounts.models import User


class AccountLoginMiddleware:

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated:
            last_activity = request.session.get('last-activity')

            too_old_time = timezone.now() - td(seconds=settings.LOGIN_INTERVAL)
            if not last_activity or parse(last_activity) < too_old_time:
                User.objects.filter(username=request.user.username).update(last_online=timezone.now(),)

            request.session['last-activity'] = timezone.now().isoformat()

        response = self.get_response(request)

        return response