

from django.urls import path, include
from chatbot import views as chat_views
from django.contrib.auth.views import LoginView, LogoutView
 
 
urlpatterns = [
    path("", chat_views.index, name="index"),
    path("", chat_views.chatPage, name="chat-page"),
    path("", chat_views.chatSelect, name="chat-select"),
    # login-section
    path("auth/login/", LoginView.as_view
         (template_name="chat/LoginPage.html"), name="login-user"),
    path("auth/logout/", LogoutView.as_view(), name="logout-user"),

]
