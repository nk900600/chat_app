import jwt,re
from django.conf import settings
from django.contrib.auth.models import User
from django.shortcuts import redirect
from user.redis import Redis
from django.shortcuts import HttpResponse



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
            token = red.get('token').decode("utf-8") # token is fetched from redis
            # print(token)
            try:
                decode = jwt.decode(token, settings.SECRET_KEY)

            except TypeError:
                return redirect('/session')

            user1 = decode['username']
            user2 = User.objects.get(username=user1)
            if user2 is not None:
                return function(*args, **kwargs)
            else:
                return redirect('/session')
        except Exception as e:
            print(e)
            return redirect('/session')
    return wrapper



