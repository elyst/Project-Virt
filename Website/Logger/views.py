from django.shortcuts import render

from .models import Entry

# Create your views here.
def LogInfo(uid, message):
    Log("Info", uid, message)
    return

def LogWarning(uid, message):
    Log("Warning", uid, message)
    return

def LogError(uid, message):
    Log("Error", uid, message)
    return

def Log(level, userid, message):
    e = Entry()
    e.userid = userid
    e.message = message
    e.severity = level
    e.save()
    return