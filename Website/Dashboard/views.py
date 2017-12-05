from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from . import forms
from VMManager.views import createNewVM

#COPY OS PATH OVER HERE !!!!!!!!!

OS = ['/LINUX', '/WINDOWS', '/APPLE']


# Create your views here.
@login_required
def index(request):
    return render(request, 'home/home.html')

@login_required
def myVM(request):
    return HttpResponse("501 Not Implemented")

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
def start_VM(request):
    return HttpResponse('Vm is gestart!')

@login_required
def accountInfo(request):
    return HttpResponse("501 Not Implemented")
      

      