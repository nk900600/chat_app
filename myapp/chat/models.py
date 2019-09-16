from django.db import models

# Create your models here.
from django.forms import forms


class Message(models.Model):

    indentifier_message_number=models.TextField(max_length=100)
    messages =models.TextField(max_length=100)
    rating = models.TextField(max_length=100)
    From = models.TextField(max_length=100)

    if indentifier_message_number == "" or messages == "" or From == "" or rating=="":
        raise forms.ValidationError(" one of the above field is empty")

    def __str__(self):
        return str(self.indentifier_message_number)

    class Meta:
        verbose_name = 'chat message'
        verbose_name_plural = 'chat messages '
