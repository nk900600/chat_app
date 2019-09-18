from django.contrib import admin
from chat.models import Message
# Register your models here.

# admin.site.register(Message)
@admin.register(Message)
class Messageadmin(admin.ModelAdmin):
    list_display = ('indentifier_message_number','messages','rating','From')