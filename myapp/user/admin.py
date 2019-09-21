from django.contrib import admin
from .models import Registration, LoggedUser

# Register your models here.


admin.site.register(LoggedUser)
@admin.register(Registration)
class Registrationadmin(admin.ModelAdmin):
    list_display = ('name','username','email','password')