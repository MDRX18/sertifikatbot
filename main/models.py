from django.db import models
# Create your models here.

class User(models.Model):
    username = models.CharField(max_length=255)
    userid = models.CharField(max_length=200)
    user_dagree = models.CharField(max_length=255, default='user')
    user_status = models.CharField(max_length=255, default='')


    def __str__(self):
        return self.username
class Sertificats(models.Model):
    ser_id = models.CharField(max_length=255, default='1')
    ser_fayl_id = models.CharField(max_length=255, default='')
    
    def __str__(self):
        return self.ser_id


    




