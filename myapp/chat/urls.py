from django.urls import path

from . import views
# from . import consumers.

urlpatterns = [
    path('chat', views.index, name='index'),
    path('chat/<str:room_name>/', views.room, name='room'),


]