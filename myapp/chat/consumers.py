# chat/consumers.py
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
import json
from django.contrib.auth.models import User
from requests import request

from chat.models import Message
from user.redis import Redis
# from user.views import ajax_token
from user.decorators import login_decorator

red=Redis()


class ChatConsumer(WebsocketConsumer):
    """
     this function is used for connecting to the websocket
    """

    def connect(self):
        """
        :return: will connect the user with the websocket
        """
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name

        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )
        self.accept()
        return self.room_name


    def disconnect(self, close_code):
        """
        :param close_code: if websocket is disconnected then it will give error
        :return: will disconnect user
        """
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket

    def receive(self, text_data):
        """
        :param text_data: data is passed
        :return: will save the message
        """
        text_data_json = json.loads(text_data)
        message = text_data_json['message']

    # Send message to room group
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message
            }
        )

    # Receive message from room group

    def chat_message(self, event):
        """
        :param event: messages receive will be checked
        :return: will dispatch chat messages
        """
        room=self.room_name
        message = event['message']

        mess = Message.objects.create(messages=message,indentifier_message_number=room)
        # Message.objects.all().filter(room)
        # json.dumps(mess)
        self.send(text_data=json.dumps({

            'message': message
        }))


    def rating(self):
        pass