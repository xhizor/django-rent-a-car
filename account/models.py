from django.db import models
from django.conf import settings


class UserProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    birth_date = models.DateField()
    address = models.CharField(null=True, blank=True, max_length=100)
    photo = models.ImageField(upload_to='users/%Y/%m/%d', blank=True)

    class Meta:
        db_table = 'profile'

    def __str__(self):
        return str(self.user.username)


