from datetime import datetime

from django.http import HttpRequest
from django.shortcuts import render


# Create your views here.

def home(request):
    """Renders the home page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'home.html'
    )


def stream(request, channel):
    """Renders the home page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'twitch.html', {'channel': channel}
    )
