from django.contrib import admin
from .models import Message, WechatUser, ServerConfig

admin.site.register(WechatUser)
admin.site.register(Message)
admin.site.register(ServerConfig)
