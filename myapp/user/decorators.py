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
    def wrapper(request,*args, **kwargs):
        """
        :return: will check token expiration
        """
        token= (request.body).decode("utf-8")
        # print(token)
        # red = Redis() # red object is created
        # token = red.get('token').decode("utf-8") # token is fetched from redis
        print(token)
        # try:
        decode = jwt.decode(token, settings.SECRET_KEY)
        # except TypeError:
        #     return redirect('/session')
        user1 = decode['username']
        user2 = User.objects.get(username=user1)
        if user2 is not None:
            print("hello")
            return function(request,*args, **kwargs)
        # else:
        #     return redirect('/session')
        else:
            return HttpResponse("hello")
    return wrapper



