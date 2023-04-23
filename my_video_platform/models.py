from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
import uuid

PROFILES_TYPES = (
    ('Premium', 'Premium'),
    ('Basic', 'Basic')
)

MOVIE_TYPE = (
    ('western', 'western'),
    ('comedy', 'comedy'),
    ('horror', 'horror'),
    ('science fiction', 'science fiction'),
    ('adventure', 'adventure')
)

class CustomUser(AbstractUser):
    profiles = models.ManyToManyField('Profile')
    username = None
    email = models.EmailField(_('email address'), unique=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []


class Profile(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=25)
    profile_type = models.CharField(max_length=30, choices=PROFILES_TYPES)
    #uuid = models.UUIDField(default=uuid.uuid4, unique=True)

    def __str__(self):
        return self.profile_type
        #return self.name + " " + self.profile_type


class UserProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, related_name='user_profile', on_delete=models.CASCADE)
    profile = models.ForeignKey(Profile, related_name='user_profile', on_delete=models.SET_NULL, null=True)

    def __str__(self):
       return self.user.username


class Subscription(models.Model):
    user_profile = models.ForeignKey(UserProfile, related_name='subscription', on_delete=models.CASCADE)
    active = models.BooleanField(default=True)

    def __str__(self):
      return self.user_profile.user.username


class Movie(models.Model):
    title = models.CharField(max_length=225)
    description = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    id = models.BigAutoField(primary_key=True)
    #uuid = models.UUIDField(default=uuid.uuid4, unique=True)
    type = models.CharField(max_length=30, choices=MOVIE_TYPE)
    videos = models.ManyToManyField('Video')
    flyer = models.ImageField(upload_to='flyers', blank=True, null=True)
    profile_type = models.CharField(max_length=30, choices=PROFILES_TYPES, blank=True, null=True)


class Video(models.Model):
    title: str = models.CharField(max_length=225, blank=True, null=True)
    file = models.FileField(upload_to='movies')
