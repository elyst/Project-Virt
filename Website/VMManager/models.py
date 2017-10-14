from django.db import models
from django.contrib import admin

# Create your models here.
class VirtualMachine(models.Model):
    VMID = models.CharField(max_length=255)
    Name = models.CharField(max_length=255)
    CPUCores = models.IntegerField()
    RAMAmount = models.IntegerField()
    DISKSize = models.IntegerField()

admin.site.register(VirtualMachine)