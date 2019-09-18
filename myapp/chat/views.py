import jwt
from django.conf import settings
from django.contrib.auth.models import User
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
    get = red.get("token").decode("utf-8")
    user=red.get("username").decode("utf-8")
    token = {
        "token": get,
        "username":user
    }
    return render(request, 'chat/index.html', token)


@login_decorator
def room(request, room_name):
    """
    :param request: user makes a request
    :param room_name: room name is called form index
    :return: will return the chat room page
    """
    if request.method=='POST':
        token=request.headers['token']
        decode = jwt.decode(token, settings.SECRET_KEY)
        username = decode['username']
        user = User.objects.get(username=username)
        return render(request, 'chat/room.html', {
            'room_name_json': mark_safe(json.dumps(room_name)),
            'user':json.dumps(user)

        })
    else:
        return render(request, 'chat/room.html', {
            'room_name_json': mark_safe(json.dumps(room_name)),

        })

