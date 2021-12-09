from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=50, null=True, blank=True)
    phoneno = models.IntegerField(unique=True,null=True, blank=True)
    email = models.EmailField(unique=True,null=True, blank=True)
    address = models.CharField(max_length=255, null=True, blank=True)
    pincode = models.IntegerField(null=True, blank=True)
    token = models.CharField(null=True, blank=True, max_length=30)
    otp = models.IntegerField(null=True, blank=True)
    dpimage = models.ImageField(upload_to='profile', null=True, blank=True)
    bio = models.CharField(max_length=100, null=True, blank=True)
    about = models.CharField(max_length=250, null=True, blank=True)
    
    ROLE_CHOICES = (
        ('admin', 'admin'),
        ('user', 'user'),
        ('player', 'player'),
    )
    role = models.CharField(max_length=20, null=True, blank=True, choices=ROLE_CHOICES)
    PLAY_CHOICES = (
        ('cricket', 'cricket'),
        ('football', 'football'),
        ('vollyball', 'volyball'),
        ('kabadi', 'kabadi'),
    )
    type = models.CharField(max_length=20, null=True, blank=True, choices=PLAY_CHOICES)

    is_active = models.BooleanField(default=False)

    def __str__(self):
        return self.name

class Feed(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=50, null=True, blank=True)
    descrption = models.CharField(max_length=250, null=True, blank=True)
    postimage = models.ImageField(upload_to='post', null=True, blank=True)
    like = models.IntegerField(null=True, blank=True,default=0)
    is_active = models.BooleanField(default=True)

    # def __str__(self):
    #     return self.user.title







