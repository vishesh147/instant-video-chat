from django.db import models

# Create your models here.

class RoomMember(models.Model):
    name = models.CharField(max_length=256)
    uid = models.CharField(max_length=256)
    room_name = models.CharField(max_length=256)

    def __str__(self):
        return self.name
