
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from .chatgpt import init_chatbot
from .forms import ChatSelector
 
def index(request, *args, **kwargs):
    if not request.user.is_authenticated:
        return redirect("login-user")
    context = {}
    form = ChatSelector()
    context['form'] = form
    if request.method == 'POST':
        # form = ChatSelector(request.GET)
        # print(form)
        temp = request.POST["chat_type"]
        print(temp)
        init_chatbot(temp)
        context = {}
        return render(request, "chat/chatPage.html", context)
    
    return render(request, "chat/index.html", context)

def chatSelect(request):
    context = {'chat_type': request.text}
    # print(f"Context Select: {context}")
    return render(request, "chat/chatPage.html", context=context)
    
def chatPage(request):
    chat_type = request.get('chat_type')
    # init_chatbot(chat_type)
    context = {}
    return render(request, "chat/chatPage.html", context)
