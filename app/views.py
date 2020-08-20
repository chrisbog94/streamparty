import json
from datetime import datetime

from django.http import HttpRequest
from django.shortcuts import render
import requests
from app.models import *

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
        'twitch.html', {'channel': streamer.name, 'viewers': viewers, 'banner': streamer.banner}
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
    streamer, created = Streamers.objects.get_or_create(name=twitch_channel)
    if created:
        streamer.display_name = display_name
        streamer.channel_id = channel_id
        streamer.bio = bio
        streamer.logo = logo
        streamer.banner = banner
        streamer.save()
    return streamer, viewers
