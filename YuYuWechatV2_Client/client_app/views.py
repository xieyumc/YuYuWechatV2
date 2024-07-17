from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from .models import Message, WechatUser, ServerConfig
import json
import requests
from django.views.decorators.csrf import csrf_exempt

def get_server_ip():
    try:
        return ServerConfig.objects.latest('id').server_ip
    except ServerConfig.DoesNotExist:
        return None  # 或者返回一个默认的IP地址

def set_server_ip(ip_address):
    ServerConfig.objects.create(server_ip=ip_address)
    return True

def home(request):
    messages = Message.objects.all()
    return render(request, 'home.html', {'messages': messages})

@csrf_exempt
def send_message(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        text = request.POST.get('text')
        server_ip = get_server_ip()  # 更新获取IP的方式

        if not server_ip:
            return JsonResponse({'status': "Server IP not set"}, status=400)

        try:
            user = WechatUser.objects.get(username=username)
        except WechatUser.DoesNotExist:
            return JsonResponse({'status': f"User {username} does not exist"}, status=400)

        data = {
            'name': username,
            'text': text
        }

        url = f'http://{server_ip}/wechat/send_message/'
        response = requests.post(
            url,
            headers={'Content-Type': 'application/json'},
            data=json.dumps(data)
        )
        return JsonResponse({'status': f"Message sent to {username}"})
    return JsonResponse({'status': "Invalid request method"}, status=405)