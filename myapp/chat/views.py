import jwt
from django.conf import settings
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.utils.safestring import mark_safe
import json
from user.models import LoggedUser
from user.redis import Redis
from .models import Message

red = Redis()


def index(request):
    """
    :param request: request is made by user
    :return: will render token which will be stored in web browser
    """
    try:
        token = request.body.decode("utf-8")
        decode = jwt.decode(token, settings.SECRET_KEY)
        username = decode['username']
        user = User.objects.get(username=username)
        # if user is not none then code will run
        if user is not None:
            logged_user = LoggedUser.objects.all().order_by('username')
            userlist = []
            for i in logged_user:
                userlist.append(i.username)
            data = {
                "token": token,
                "username": user,
                "userlist": userlist
            }
            return render(request, 'chat/index.html',data)
    except Exception as e:
        return redirect("/session")


def room(request, room_name):
    """
    :param request: user makes a request
    :param room_name: room name is called form index
    :return: will return the chat room page
    """
    if request.method == 'POST':
        token = request.body.decode('utf-8')
        decode = jwt.decode(token, settings.SECRET_KEY)
        username = decode['username']
        user = User.objects.get(username=username)
        # if user is not none then code will run
        if user is not None:
            userlist = []
            logged_user = LoggedUser.objects.all().order_by('username')
            for i in logged_user:
                userlist.append(i.username)
            return render(request, 'chat/room.html', {
                'room_name_json': mark_safe(json.dumps(room_name)),
                'user': user,
                'userlist': userlist
            })
        else:
            return redirect("/session")
    else:
        mess = Message.objects.filter(indentifier_message_number=room_name).values('messages')
        m = list(mess)
        return render(request, 'chat/room.html', {
            'room_name_json': room_name,
            'messages': mark_safe(json.dumps(m))
        })
