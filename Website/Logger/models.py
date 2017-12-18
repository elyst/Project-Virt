from django.db import models

# Create your models here.
class Entry(models.Model):
    severity = models.CharField(max_length=10, default="Info")
    message = models.CharField(max_length=1024, default="No Message")
    date = models.DateTimeField(auto_now=True)
