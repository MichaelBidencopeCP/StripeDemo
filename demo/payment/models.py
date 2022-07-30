from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    active_sub = models.BooleanField(default=False)
    last_pament = models.DateField(blank=True, null=True)

    def __str__(self):
        return self.user.username



