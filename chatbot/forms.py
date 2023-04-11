from django import forms
from django.db import models

chat_selector = (
    ('zero', 'Zero Context Chat'),
    ('hiking', 'Hiking Chat'),
    ('openai', 'OpenAI Embeddings Chat')
)

class ChatSelector(forms.Form):
    chat_type = forms.ChoiceField(choices=chat_selector)

