from django.db import models
from django.contrib.auth import get_user_model
# Create your models here.

User = get_user_model()

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.IntegerField()
    city = models.CharField(max_length=20)
    state = models.CharField(max_length=20)
    postal_code = models.IntegerField()
    profile_picture = models.ImageField(upload_to='user_profiles/')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username

class SavedAddress(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    address = models.TextField(max_length=200)

    def __str__(self):
        return f'{self.user.username} --> {self.address}'