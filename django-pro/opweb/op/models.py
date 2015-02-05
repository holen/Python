from django.db import models
from django.utils import timezone

# Create your models here.
class Machine(models.Model):
    machine_name = models.CharField(max_length=200)
    machine_ip = models.CharField(max_length=15)
    machine_user = models.CharField(max_length=200)
    machine_passwd = models.CharField(max_length=200)
    machine_update_date = models.DateField('last_update_time')
    #machine_update_date = models.DateField(default=timezone.now())
    #machine_update_date = models.DateField(auto_now_add=True)
    
    def __str__(self):
	return self.machine_name

class Load(models.Model):
    load_id = models.IntegerField(default=1)
    load_server = models.CharField(max_length=200)
    load_ip = models.CharField(max_length=15)
    load_str = models.CharField(max_length=200)
    load_ip_count = models.IntegerField(default=15)
    load_update_date = models.DateField('update_time')
    #load_update_date = models.DateField(auto_now_add=True)

    def __str__(self):
	return str(self.load_id)


