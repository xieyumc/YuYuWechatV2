from django.db import models


class WechatUser(models.Model):
    username = models.CharField(max_length=255, unique=True)
    wechatid = models.CharField(max_length=255, unique=True, blank=True, null=True)
    date_added = models.DateTimeField(blank=True, null=True)
    def __str__(self):
        return self.username


class Message(models.Model):
    user = models.ForeignKey(WechatUser, on_delete=models.CASCADE)
    text = models.TextField()

    def __str__(self):
        return self.user.username
