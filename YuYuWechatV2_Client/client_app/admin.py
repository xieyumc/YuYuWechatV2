from django.contrib import admin
from .models import Message, WechatUser

admin.site.register(WechatUser)
admin.site.register(Message)