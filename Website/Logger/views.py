from django.shortcuts import render

from .models import Entry

# Create your views here.
def LogInfo(message):
    e = Entry()
    e.message = message
    e.severity = "Info"
    e.save()
    return

def LogWarning(message):
    e = Entry()
    e.message = message
    e.severity = "Warning"
    e.save()
    return

def LogError(message):
    e = Entry()
    e.message = message
    e.severity = "Error"
    e.save()
    return
