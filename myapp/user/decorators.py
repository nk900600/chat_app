import jwt
from django.conf import settings
from django.contrib.auth.models import User
from django.shortcuts import redirect
from user.redis import Redis


def login_decorator(function):
    """
    :param function: function is called
    :return: will check token expiration
    """
    def wrapper(*args, **kwargs):
        """
        :return: will check token expiration
        """
        try:
            red = Redis() # red object is created
            token = red.get("token")   # token is fetched from redis
            try:
                decode = jwt.decode(token, settings.SECRET_KEY)
            except TypeError:
                return redirect('/session')
            username = decode['username']
            user = User.objects.get(username=username)
            if user is not None:
                return function(*args, **kwargs)
            else:
                return redirect('/session')
        except Exception:
            return redirect('/session')

    return wrapper
