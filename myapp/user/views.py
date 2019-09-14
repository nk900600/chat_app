from smtplib import SMTPAuthenticationError
import redis

from user.decorators import login_decorator
from .models import Registration
import requests, jwt
from django.conf import settings
from django.contrib.auth.models import User, auth
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail, EmailMessage
from django.shortcuts import render, redirect
from django.contrib import messages
from django.template.loader import render_to_string
from django.views.decorators.csrf import csrf_exempt
from rest_framework_jwt.settings import api_settings

AUTH_ENDPOINT = "http://127.0.0.1:8000/auth/jwt/"

jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
jwt_response_payload_handler = api_settings.JWT_RESPONSE_PAYLOAD_HANDLER
redis = redis.Redis("localhost")


def home(request):
    return render(request, 'user/index.html')



def registration(request):
    if request.method == 'POST':
        firstname = request.POST['name']
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password1']

        if firstname == "" or username == "" or email == "" or password == "":
            messages.info(request, "one of the above field is empty")
            return redirect('/registration')

        elif User.objects.filter(username=username).exists():
            messages.info(request, "user already exists")
            return redirect('/registration')
        elif User.objects.filter(email=email).exists():
            messages.info(request, "email already exists")
            return redirect('/registration')
        else:
            user_info = Registration(username=username, email=email, password=password)
            user_info.save()
            user = User.objects.create_user(username=username, email=email, password=password,
                                            first_name=firstname)
            user.save()
            if user is not None:
                data = {
                    'username': username,
                    'password': password
                }
                r = requests.post(AUTH_ENDPOINT, data=data)
                try:
                    key = r.json()['token']
                except KeyError:
                    messages.info(request, "please check the password entered")
                    return redirect('/registration')

                # z = jwt.decode(r.json()['token'], settings.SECRET_KEY)
                mail_subject = "Activate your account by clicking below link"
                mail_message = render_to_string('user/activatetoken.html', {
                    'user': user.username,
                    'domain': get_current_site(request).domain,
                    'token': key
                })
                recipientemail = user.email
                email = EmailMessage(mail_subject, mail_message, to=[recipientemail])
                try:
                    email.send()
                except SMTPAuthenticationError:
                    messages.info(request, "please enter vaild email address")
                    return redirect('/registration')

                messages.info(request, "please check your mail for the validation link ")
                return redirect('/registration')
    else:
        return render(request, 'user/registration.html')


# @login_decorator
def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password1']

        if username == "" or password == "":
            messages.info(request, "one of the above field is empty")
            return redirect('/login')
        user = auth.authenticate(username=username, password=password)
        if user is not None:
            data = {
                'username': username,
                'password': password
            }
            r = requests.post(AUTH_ENDPOINT, data=data)
            print(r.json()['token'])
            auth.login(request, user)
            z = jwt.decode(r.json()['token'], settings.SECRET_KEY)
            print(z['username'])
            smd = {
                'success': True,
                'message': "successfully logged",
                'data': [r.json()['token']]

            }
            messages.info(request, "logged in")
            red=redis.set('token', r.json()['token'])
            get=redis.get('token')
            print(get)

            # return Response(json.dumps(smd['data']))
            return redirect('/chat')
        else:
            messages.info(request, "password error")
            return redirect('/login')
    else:
        return render(request, 'user/login.html')


@csrf_exempt
def forgotpassword(request):
    if request.method == 'POST':
        email = request.POST["email"]
        if email == "":
            messages.info(request, "please enter a vaild email address")
            return redirect('/login/forgotpassword')
        else:
            user = User.objects.get(email=email)
            user_info = Registration.objects.get(email=email)
            # user.get(username,password)
            if user is not None:
                username = user.username
                password = user_info.password
                print(username, password)
                data = {
                    'username': username,
                    'password': password
                }
                r = requests.post(AUTH_ENDPOINT, data=data)
                print(r)
                key = r.json()['token']
                mail_subject = "Activate your account by clicking below link"
                mail_message = render_to_string('user/reset_password_token_link.html', {
                    'user': user.username,
                    'domain': get_current_site(request).domain,
                    'token': key
                })
                recipientemail = user.email
                email = EmailMessage(mail_subject, mail_message, to=[recipientemail])
                email.send()
                messages.info(request, "please check your mail for the resetting password ")
                return redirect('/login/forgotpassword')
            else:
                messages.info(request, 'not a registered email address')
                return redirect('/login/forgotpassword')
    else:
        return render(request, 'user/forgotpassword.html')


def activate(request, token):
    try:
        decode = jwt.decode(token, settings.SECRET_KEY)
        username = decode['username']
        user = User.objects.get(username=username)
        if user is not None:
            user.is_active = True
            user.save()
            messages.info(request, "your account is active now")
            return redirect('/login')
        else:
            messages.info(request, 'was not able to sent the email')
            return redirect('/registration')
    except KeyError:
        messages.info(request, 'was not able to sent the email')
        return redirect('/registration')


def reset_password(request, token):
    try:
        decode = jwt.decode(token, settings.SECRET_KEY)
        username = decode['username']
        user = User.objects.get(username=username)
        print(user)
        if user is not None:
            context = {'userReset': user.username}
            print(context)
            return redirect('/login/forgotpassword/resetpassword/' + str(user))
        else:
            messages.info(request, 'was not able to sent the email')
            return redirect('login/forgotpassword')
    except KeyError:
        messages.info(request, 'was not able to sent the email')
        return redirect('login/forgotpassword')


def resetpassword(request, userReset):
    if request.method == 'POST':
        print(userReset)
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        if password1 == "" or password2 == "":
            messages.info(request, "please check the re entered password again")
            return redirect("/login/forgotpassword/resetpassword/" + str(userReset))
            # return reverse('resetpassword', args={userReset})
        elif password2 != password1:
            messages.info(request, "please check the re entered password again")
            return redirect("/login/forgotpassword/resetpassword/" + str(userReset))
        else:
            user = User.objects.get(username=userReset)
            user.set_password(password1)
            user.save()
            messages.info(request, "password reset done")
            return redirect("/login")
    else:
        return render(request, 'user/resetpassword.html')




@login_decorator
def logout(request):
        redis.delete("token")
        messages.info(request,"logged out")
        return render(request,'user/logout.html')

