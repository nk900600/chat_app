import jwt
from django.conf import settings
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.utils.safestring import mark_safe
import json
from user.decorators import login_decorator
from user.models import LoggedUser
from user.redis import Redis
from .models import Message
red = Redis()




@login_decorator
def index(request):
    """
    :param request: request is made by user
    :return: will render token which will be stored in web browser
    """
    user=request.user
    username=user.username
    token = red.get('token').decode("utf-8")
    logged_user = LoggedUser.objects.all().order_by('username')

    userlist=[]
    for i in logged_user:
        userlist.append(i.username)
    data = {
        "token": token,
        "username":user,
        "userlist":userlist
    }
    print(userlist)
    return render(request, 'chat/index.html', data)

@login_decorator
def room(request, room_name):
    """
    :param request: user makes a request
    :param room_name: room name is called form index
    :return: will return the chat room page
    """
    if request.method=='POST':
        token=request.headers['token']
        print(token)
        decode = jwt.decode(token, settings.SECRET_KEY)
        username = decode['username']
        user = User.objects.get(username=username)
        if user is not None:

            userlist = []
            logged_user = LoggedUser.objects.all().order_by('username')
            for i in logged_user:
                userlist.append(i.username)
            return render(request, 'chat/room.html', {
                'room_name_json': mark_safe(json.dumps(room_name)),
                'user':json.dumps(user),
                'userlist':userlist
            })
        else:
            return redirect('/session')
    else:
        return render(request, 'chat/room.html', {
            'room_name_json': mark_safe(json.dumps(room_name)),
        })

