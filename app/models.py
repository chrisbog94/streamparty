from django.db import models

# Create your models here.
class Streamers(models.Model):
    display_name = models.CharField(max_length=30, null=True)
    channel_id = models.IntegerField(null=True)
    name = models.TextField(null=True)
    bio = models.TextField(null=True)
    logo = models.URLField(max_length=200, null=True)
    banner = models.URLField(max_length=200, null=True)


class Avatars(models.Model):
    name = models.CharField(max_length=30)
    image = models.URLField(max_length=200)
    