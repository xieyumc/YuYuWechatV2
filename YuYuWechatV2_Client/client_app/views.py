from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from .models import Message
import json
import requests

def home(request):
    messages = Message.objects.all()
    return render(request, 'home.html', {'messages': messages})

def send_message(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        text = request.POST.get('text')
        data = {
            'name': username,
            'text': text
        }
        server_ip = request.POST.get('server_ip')
        url = f'http://{server_ip}/wechat/send_message/'
        response = requests.post(
            url,
            headers={'Content-Type': 'application/json'},
            data=json.dumps(data)
        )
        return HttpResponse(f"Message sent to {username}: {response.json()}")
    return HttpResponse("Invalid request method", status=405)
