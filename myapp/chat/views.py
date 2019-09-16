from django.shortcuts import render, redirect
from django.utils.safestring import mark_safe
import json
from user.decorators import login_decorator
from user.redis import Redis
red = Redis()


@login_decorator
def index(request):
    """
    :param request: request is made by user
    :return: will render token which will be stored in web browser
    """
    get = red.get('token')
    token = {
        "token": get,
        "username":red.get('username')
    }
    return render(request, 'chat/index.html', token)


@login_decorator
def room(request, room_name):
    """
    :param request: user makes a request
    :param room_name: room name is called form index
    :return: will return the chat room page
    """
    return render(request, 'chat/room.html', {
        'room_name_json': mark_safe(json.dumps(room_name)),
    })
