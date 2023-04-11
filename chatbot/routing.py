from django.urls import re_path , include
from chatbot.consumers import ChatConsumer

# Here, "" is routing to the URL ChatConsumer which
# will handle the chat functionality.
websocket_urlpatterns = [
    re_path("" , ChatConsumer.as_asgi()) ,
]
