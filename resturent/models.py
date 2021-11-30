from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    name = models.CharField(max_length=50, null=True, blank=True)
    phoneno = models.IntegerField(unique=True,null=True, blank=True)
    email = models.EmailField(unique=True,null=True, blank=True)
    reffer_by = models.CharField(max_length=5, null=True, blank=True)
    refferal_code = models.CharField(max_length=5, null=True, blank=True)
    address = models.CharField(max_length=255, null=True, blank=True)
    pincode = models.IntegerField(null=True, blank=True)
    token = models.CharField(null=True, blank=True, max_length=30)
    otp = models.IntegerField(null=True, blank=True)
    dpimage = models.ImageField(upload_to='profile', null=True, blank=True)
    bio = models.CharField(max_length=5, null=True, blank=True)
    about = models.CharField(max_length=5, null=True, blank=True)
    is_active = models.BooleanField(default=False)





    def __str__(self):
        return self.name
