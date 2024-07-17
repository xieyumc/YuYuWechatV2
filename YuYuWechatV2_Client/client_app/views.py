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


@csrf_exempt
def set_server_ip(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        server_ip = data.get('server_ip')
        if server_ip:
            # 删除现有的所有IP记录
            ServerConfig.objects.all().delete()
            # 添加新的IP记录
            ServerConfig.objects.create(server_ip=server_ip)
            return JsonResponse({'status': f"Server IP set to {server_ip}"})
        else:
            return JsonResponse({'status': "No IP address provided"}, status=400)
    return JsonResponse({'status': "Invalid request method"}, status=405)


def home(request):
    messages = Message.objects.all()
    groups = Message.objects.values_list('group', flat=True).distinct()  # 获取所有分组
    return render(request, 'home.html', {'messages': messages, 'groups': groups})


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
