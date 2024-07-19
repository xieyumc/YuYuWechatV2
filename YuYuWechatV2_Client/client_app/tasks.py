from celery import shared_task
from django.utils import timezone
from .models import ScheduledMessage, ServerConfig
import requests
import json


@shared_task
def check_and_send_messages():
    # 获取当前时间
    now = timezone.now()

    # 查询所有还需要执行的消息
    messages = ScheduledMessage.objects.filter(execution_count__gt=0)

    # 尝试获取服务器IP
    try:
        server_config = ServerConfig.objects.first()
        if not server_config:
            print("Server IP not set")
            return
        server_ip = server_config.server_ip
    except ServerConfig.DoesNotExist:
        print("Server IP configuration is missing")
        return

    for message in messages:
        # 此处假设 cron_expression 是以分钟为单位执行的简单表达式
        # 例如，'*/5' 表示每5分钟执行一次
        if check_cron(now, message.cron_expression):
            # 构建请求数据和发送消息
            data = {
                'name': message.user.username,
                'text': message.text
            }
            send_message(data, server_ip)
            # 更新消息状态
            message.execution_count -= 1
            message.last_executed = now
            message.save()


def check_cron(current_time, cron_expression):
    """简单的cron表达式检查，仅适用于分钟"""
    if cron_expression.startswith('*/'):
        interval = int(cron_expression.split('/')[1])
        return current_time.minute % interval == 0
    return False


def send_message(data, server_ip):
    """调用视图发送消息"""
    url = f'http://{server_ip}/wechat/send_message/'
    response = requests.post(
        url,
        headers={'Content-Type': 'application/json'},
        data=json.dumps(data)

    )
    print(response.text)