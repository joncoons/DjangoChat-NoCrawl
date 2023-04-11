from asgiref.sync import async_to_sync
from celery import shared_task
from channels.layers import get_channel_layer
from chatbot.chatgpt import new_message

channel_layer = get_channel_layer()

@shared_task
def get_response(channel_layer, username, message):
    response =  new_message(username, message)
    print(f"ChatGPT response: {response}")
