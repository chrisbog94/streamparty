from django.contrib import admin
from app.models import *

# Register your models here.
admin.site.register(Streamer)
admin.site.register(UsertoAvatar)
admin.site.register(Avatar)
admin.site.register(TwitchUser)
admin.site.register(ReleasePack)