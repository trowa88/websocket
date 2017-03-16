from django.db import models


# Create your models here.
class ChatUser(models.Model):
    user_id = models.CharField(max_length=50)

    def __str__(self):
        return self.user_id
