from django.db import models
from django import forms


class Registration(models.Model):

    name = models.CharField(max_length=100)
    username = models.CharField(max_length=100)
    email = models.EmailField()
    password = models.CharField(max_length=100)
    messages=models.TextField(max_length=1000)

    if name == "" or username == "" or email == "" or password == "":
        raise forms.ValidationError(" one of the above field is empty")

    def __str__(self):
        return str(self.name)

    class Meta:
        verbose_name = 'user detail'
        verbose_name_plural = 'user details '
