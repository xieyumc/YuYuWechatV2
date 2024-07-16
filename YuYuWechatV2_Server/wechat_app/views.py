from django.shortcuts import render

# Create your views here.
from django.shortcuts import render

# Create your views here.
# wechat_app/views.py

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
import comtypes

from .ui_auto_wechat import WeChat

# 初始化 WeChat 类实例
wechat = WeChat(path="C:/Program Files/Tencent/WeChat/WeChat.exe", locale="zh-CN")

@csrf_exempt
def send_message(request):


    if request.method == 'POST':
        try:
            comtypes.CoInitialize()

            data = json.loads(request.body)
            name = data['name']
            text = data['text']
            wechat.send_msg(name, text)
            return JsonResponse({'status': 'Message sent'}, status=200)
        except (KeyError, json.JSONDecodeError):
            return JsonResponse({'error': 'Invalid request, missing name or text'}, status=400)
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=405)
@csrf_exempt
def ping(request):
    return JsonResponse({'status': 'pong'})