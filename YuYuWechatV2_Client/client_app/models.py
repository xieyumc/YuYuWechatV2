from django.db import models

class Message(models.Model):
    username = models.CharField(max_length=255)
    text = models.TextField()

    def __str__(self):
        return self.username