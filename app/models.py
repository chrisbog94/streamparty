from __future__ import unicode_literals
from django.conf import settings

from django.db import models


# Create your models here.
class Streamer(models.Model):
    display_name = models.CharField(max_length=30, null=True)
    channel_id = models.IntegerField(null=True)
    name = models.TextField(null=True)
    bio = models.TextField(null=True)
    logo = models.URLField(max_length=200, null=True)
    banner = models.URLField(max_length=200, null=True)


class TwitchUser(models.Model):
    display_name = models.CharField(max_length=30, null=True)
    email_address = models.EmailField(null=True)
    streamparty_member = models.BooleanField(default=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)


class ReleasePack(models.Model):
    name = models.CharField(null=True, max_length=30)
    release_date = models.DateTimeField(null=True)


class Avatar(models.Model):
    name = models.CharField(max_length=30)
    back = models.URLField(max_length=200)
    front = models.URLField(max_length=200)
    shadow = models.URLField(max_length=200)
    frames = models.IntegerField(null=True, default=20)
    width = models.IntegerField(null=True, default=3400)
    height = models.IntegerField(null=True, default=220)
    release_pack = models.ForeignKey(ReleasePack, on_delete=models.DO_NOTHING, null=True)
    rarity = models.IntegerField(null=True, default=1)


class UsertoAvatar(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)
    avatar = models.ForeignKey(Avatar, on_delete=models.DO_NOTHING, null=True)
    active = models.BooleanField(default=False)
