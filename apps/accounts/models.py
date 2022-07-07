from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from django.utils.timesince import timesince

class User(AbstractUser):
    first_name = None
    last_name = None
    email = models.EmailField(_("email address"))
    date_joined = models.DateTimeField(_("date joined"), default=timezone.now)
    reputation = models.PositiveIntegerField(_("reputation"), default=0)
    last_online = models.DateTimeField(_("last online"), default=timezone.now)
    bio = models.CharField( _("bio"), max_length = 500, null=True)
    avatar = models.ImageField(upload_to='avatars/', null=True)

    def __str__(self) -> str:
        return self.username
    
    @property
    def last_activity(self):
        period = timesince(self.last_online).replace('\xa0', ' ')
        if period.split()[1] == 'minutes' and int(period.split()[0]) <= 10:
            return 'online'
        return period + ' ago'
    
    @property
    def joined(self):
        if self.date_joined.year == timezone.now().year:
            return self.date_joined.strftime('%d %b')
        return self.date_joined.strftime('%d %b, %Y')
    
    @property
    def avatar_url(self):
        if self.avatar:
            return self.avatar.url
        return 'https://discuss.flarum.org/assets/avatars/oftWsKuTIyGBpF47.png'
    
    class Meta:
        ordering = ["-date_joined"]

