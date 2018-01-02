from django.shortcuts import render, HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

from . import forms
from VMManager.views import createNewVM, start, stop, reboot, suspend, deleteVM, VMstate # Add defs 
from VMManager.models import VirtualMachine
import os
import os
import re

#COPY OS PATH OVER HERE !!!!!!!!!

OS = ['/home/jurrewolff/Desktop/iso/ubuntu-16.04.3-server-amd64.iso', '/home/jurrewolff/Desktop/iso/linuxmint-18.2-cinnamon-64bit.iso', '/APPLE']


# Create your views here.
@login_required
def index(request):
    user = str(request.user)
    data = VirtualMachine.objects.filter(User__exact=user)
    ram_count = 0
    vm_count = 0
    for value in data:
        vm_count += 1
        ram_count += value.RAMAmount

    ram_count = (8000000 - ram_count) / 1000000
    ram_count = str(ram_count) + ' GB'
    
    return render(request, 'home/home.html', {'ram_count' : ram_count, 'vm_count': vm_count})

@login_required
def myVM(request):
    user = request.user
    # Prepare data for vm list
    if request.method == "GET":
        VMstate(user)
        data = VirtualMachine.objects.filter(User__exact=user)  # Get database data for currently logged in user  
        return render(request, 'home/myVM.html', {'data': data})

    elif request.method == "POST":
        if request.POST.get("start", None):
            name = request.POST.get("start", None)
            print("start")
            start(name)
        elif request.POST.get("stop", None):
            name = request.POST.get("stop", None)
            print("stop")
            stop(name)
        elif request.POST.get("reboot", None):
            name = request.POST.get("reboot", None)
            print("reboot")
            reboot(name)
        elif request.POST.get("suspend", None):
            name = request.POST.get("suspend", None)
            print("suspend")
            suspend(name)
        elif request.POST.get("deleteVM", None):
            name = request.POST.get("deleteVM", None)
            print("deletetet")
            deleteVM(name) 

        VMstate(user)
        data = VirtualMachine.objects.filter(User__exact=user)
        
       
        return render(request, 'home/myVM.html', {'data': data})


@login_required
def createVM(request):
    if request.method == "GET":
        # Generate form and show CreateVM to the user
        form = forms.NewVMForm()

        return render(request, "home/CreateVM.html", {'form': form})
    elif request.method == "POST":
        # Populate, verify and process the input data
        form = forms.NewVMForm(request.POST)

        #Check which os has been chosen
        options = request.POST.get("options", None)
        if options in ["1", "2", "3"]:
            OS_Choice = OS[(int(options)- 1)]

        #If everything ok, create VM
        if form.is_valid():
            if createNewVM(
                request,
                form.cleaned_data["VirtualMachineName"],
                form.cleaned_data["CPUCores"],
                form.cleaned_data["RAMAmount"],
                form.cleaned_data["DiskSize"],
                OS_Choice) != True:
                return render(request, "home/CreateVM.html", {'alert' : "danger", 'form': form})
      
        return render(request, "home/CreateVM.html", {'alert' : "success", 'form': form})

@login_required
def accountInfo(request):
    return HttpResponse("501 Not Implemented")