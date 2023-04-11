import json
import time
# from channels.generic.websocket import AsyncWebsocketConsumer
from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync
from .tasks import get_response
from .chatgpt import init_chatbot, new_message


class ChatConsumer(WebsocketConsumer):
    # def __init__(self):
    #     self.room_group_name = "group_chat"

    def connect(self):
        self.room_group_name = "group_chat"
        async_to_sync(self.channel_layer.group_add)(
        self.room_group_name,
        self.channel_name
        )
        self.accept()

    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(
        self.room_group_name,
        self.channel_name
                )

    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]
        username = text_data_json["username"]

        async_to_sync(self.channel_layer.group_send)(
			self.room_group_name,{
				"type" : "sendMessage" ,
				"message" : message ,
				"username" : username ,
			})
        
        response =  new_message(username, message)

        async_to_sync(self.channel_layer.group_send)(
			self.room_group_name,{
				"type" : "sendMessage" ,
				"message" : response ,
				"username" : "ChatGPT" ,
			})

        # get_response.delay(self.channel_name, username, message)
    
    def sendMessage(self, event):
        message = event["message"]
        username = event["username"]
        self.send(text_data=json.dumps({"message": message, "username": username}))