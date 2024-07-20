from django.urls import path
from .views import home, send_message, set_server_ip, schedule_management

urlpatterns = [
    path('', home, name='home'),
    path('send_message/', send_message, name='send_message'),
    path('set_server_ip/', set_server_ip, name='set_server_ip'),  # 新增的URL路由
    path('schedule_management/', schedule_management, name='schedule_management'),  # 新增的URL路由

]