from django.db import models
from django.utils import timezone
from django.urls import reverse
from django_extensions.db.models import (TimeStampedModel,
                                         TitleDescriptionModel)
from django.contrib.auth.models import User
from phonenumber_field.modelfields import PhoneNumberField

# Create your models here.
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token

import requests
from urllib.request import urlopen
from django.core.files import File
from django.core.files.temp import NamedTemporaryFile

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)


class UserProfile(TimeStampedModel):
    email = models.EmailField(max_length=255, blank=True, null=True)
    # phone = models.CharField(max_length=20)
    phone = PhoneNumberField(null=False, blank=False, unique=True)
    pic = models.ImageField(upload_to='user_profile', blank=True, null=True)
    user = models.OneToOneField(User, on_delete=models.PROTECT)
    otp = models.CharField(max_length=10,blank=True, null=True)
    is_verified = models.BooleanField(default=False)
    from_to = models.DateField(null=False, blank=False)
    valid_to = models.DateField(null=True, blank=True)

    def __str__(self):
        return 'User Profile for: ' + self.user.username


class Excerciseslist(TimeStampedModel):
    bodypart = models.CharField(max_length=255, blank=True, null=True)
    equipment = models.CharField(max_length=255, blank=True, null=True)
    gif_url = models.URLField()
    image = models.ImageField(upload_to='excercise_img', blank=True, null=True)
    name = models.CharField(max_length=255, blank=True, null=True)
    target = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.bodypart

