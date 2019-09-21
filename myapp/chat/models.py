from django.db import models

# Create your models here.
from django.forms import forms


class Message(models.Model):

    indentifier_message_number=models.TextField(max_length=100,default="foobar")
    messages =models.TextField(max_length=1000,default="foobar")
    rating = models.TextField(max_length=100,default="foobar")
    From = models.TextField(max_length=100,default="foobar")
    # time=models.DateTimeField(auto_now_add=True)


    class Meta:
        verbose_name = 'message log'
        verbose_name_plural = 'message log '
