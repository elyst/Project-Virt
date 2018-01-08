from django.db import models
from django.contrib import admin

# Create your models here.
class VirtualMachine(models.Model):
    VMID = models.CharField(max_length=255)
    User = models.CharField(default="null", max_length=255)
    Name = models.CharField(max_length=255)
    CPUCores = models.IntegerField()
    RAMAmount = models.IntegerField()
    DISKSize = models.IntegerField()
    State = models.CharField(default="running", max_length= 50)
    Date = models.DateTimeField(auto_now_add=True)
    SSH_User = models.CharField(default="null", max_length=5)


admin.site.register(VirtualMachine)