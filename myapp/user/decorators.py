import redis
import jwt
import requests
from django.conf import settings
from django.contrib.auth.models import User
from django.core.checks import messages
from django.shortcuts import redirect


def login_decorator(function):
    def wrapper(*args, **kwargs):
        token = redis.get("token")
        decode = jwt.decode(token, settings.SECRET_KEY)
        username = decode['username']
        user = User.objects.get(username=username)
        if user is not None:
            return function(*args, **kwargs)
        else:
            messages.info(requests, "username is not vaild")
            return redirect("/login")
    return wrapper