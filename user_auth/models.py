from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.

class CustomUser(AbstractUser):
    is_email_verified = models.BooleanField(default=False)

    class Meta:
        db_table = 'custom_user'

