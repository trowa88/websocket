import uuid

from django.contrib.auth.models import User
from django.contrib.sessions.models import Session
from django.shortcuts import render


# Create your views here.
from django.utils import timezone

from chat.models import ChatUser


def chat_home(request):
    user_name = str(uuid.uuid1()).replace('-', '')
    user_list = ChatUser.objects.values_list('user_id', flat=True)
    return render(request, 'home.html', {
        'user_name': user_name,
        'user_list': user_list
    })
