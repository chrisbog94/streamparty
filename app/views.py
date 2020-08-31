import json
from datetime import datetime

from django.contrib.auth.models import User
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
import requests
from app.models import *
from django.views.decorators.csrf import csrf_exempt
from django.core import serializers

twitch_client_id = 'mkfo0b5r43pvu51772vyxmlohqv4hb'
default_banner = '/assets/images/backdrops/default_backdrop.jpg'


# Create your views here.
def home(request):
    streamer, viewers = getStream(featured=True, twitch_channel='')
    if streamer.banner is None:
        streamer.banner = default_banner
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'index.html', {'channel': streamer.name, 'viewers': viewers, 'banner': streamer.banner}
    )


def stream(request, channel):
    streamer, viewers = getStream(featured=False, twitch_channel=channel)
    if streamer.banner is None:
        streamer.banner = default_banner
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'index.html', {'channel': streamer.name, 'viewers': viewers, 'banner': streamer.banner}
    )


# returns streamer, viewers
def getStream(featured=False, twitch_channel=''):
    viewers = 1
    twitch_headers = {'Accept': 'application/vnd.twitchtv.v5+json', 'Client-ID': twitch_client_id}
    if featured:
        featured_response = requests.request("GET", "https://api.twitch.tv/kraken/streams/featured?limit=1",
                                             headers=twitch_headers)
        stream_response = json.loads(featured_response.text)

        viewers = stream_response['featured'][0]['stream']['viewers']
        display_name = stream_response['featured'][0]['stream']['channel']['display_name']
        channel_id = stream_response['featured'][0]['stream']['channel']['_id']
        twitch_channel = stream_response['featured'][0]['stream']['channel']['name']
        bio = stream_response['featured'][0]['stream']['channel']['description']
        logo = stream_response['featured'][0]['stream']['channel']['logo']
        banner = stream_response['featured'][0]['stream']['channel']['profile_banner']

    elif not featured and twitch_channel:
        twitch_user_lookup_response = requests.request("GET",
                                                       "https://api.twitch.tv/kraken/users?login=" + twitch_channel,
                                                       headers=twitch_headers)
        twitch_user_lookup = json.loads(twitch_user_lookup_response.text)
        twitch_id = twitch_user_lookup['users'][0]['_id']
        twitch_channel_lookup_response = requests.request("GET",
                                                          "https://api.twitch.tv/kraken/streams/" + str(twitch_id),
                                                          headers=twitch_headers)
        twitch_channel_lookup = json.loads(twitch_channel_lookup_response.text)
        if twitch_channel_lookup['stream'] != None:
            viewers = twitch_channel_lookup['stream']['viewers']
            display_name = twitch_channel_lookup['stream']['channel']['display_name']
            channel_id = twitch_channel_lookup['stream']['channel']['_id']
            twitch_channel = twitch_channel_lookup['stream']['channel']['name']
            bio = twitch_channel_lookup['stream']['channel']['description']
            logo = twitch_channel_lookup['stream']['channel']['logo']
            banner = twitch_channel_lookup['stream']['channel']['profile_banner']

    if viewers > 5000:
        viewers = 5000
    streamer, created = Streamer.objects.get_or_create(name=twitch_channel)
    if created:
        streamer.display_name = display_name
        streamer.channel_id = channel_id
        streamer.bio = bio
        streamer.logo = logo
        streamer.banner = banner
        streamer.save()
    return streamer, viewers
    pass


def getViewers():
    pass


@csrf_exempt
def receiveViewers(request):
    if 'viewers[]' in request.POST:
        avatar_list = {}
        viewers = request.POST.getlist('viewers[]')
        if len(viewers) <= 25:
            for viewer in viewers:
                user_lookup = User.objects.filter(username=viewer).first()
                if user_lookup:
                    avatar_lookup = UsertoAvatar.objects.filter(user_id=user_lookup.pk).first()
                    if avatar_lookup:
                        avatar = Avatar.objects.filter(width=3400).filter(height=220).order_by('?').first()
                        avatar_list.update({viewer: [avatar.back, avatar.height, avatar.width, avatar.frames, 'VIP']})
                else:
                    avatar = Avatar.objects.filter(release_pack__name='base')
                    avatar_list.update({viewer: [avatar.back, avatar.height, avatar.width, avatar.frames, 'PLEB']})
                # avatar_list.append();
            avatars = json.dumps(avatar_list)
            return HttpResponse(avatars, content_type="text/json-comment-filtered")
    else:
        return None

# import os
# from app.models import Avatar
# base_dir = './assets/images/avatars/back'
# folders = os.listdir(base_dir)
# for folder in folders:
#     rp, created = ReleasePack.objects.get_or_create(name=folder)
#     files = os.listdir(base_dir + '/' + folder)
#     for file in files:
#         new_avatar = Avatar.objects.create(
#             name=file[:-4],
#             back='https://streamparty.me/assets/images/avatars/back/' + folder + '/' + file,
#             front='https://streamparty.me/assets/images/avatars/front/' + file,
#             shadow='https://streamparty.me/assets/images/avatars/shadow/' + file,
#             frames='20',
#             width='3400',
#             height='220',
#             rarity='1',
#             release_pack=rp
#         )
#         new_avatar.save()
#         print(file)
