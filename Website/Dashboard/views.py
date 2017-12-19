from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.mail import EmailMessage
from django.contrib.auth.models import User

from . import forms
from VMManager.views import createNewVM
from VMManager.models import VirtualMachine
import string, random

#COPY OS PATH OVER HERE !!!!!!!!!

OS = ['/LINUX', '/WINDOWS', '/APPLE']


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
        
        #Generate random ssh user
        ssh_user = generateRandChar(5)
        rand_password = generateRandChar(8)

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
        
        #Sendmail with SSH credentials
        sendMail(request, ssh_user, rand_password)    

        return render(request, "home/CreateVM.html", {'alert' : "success", 'form': form})

@login_required
def start_VM(request):
    return HttpResponse('Vm is gestart!')

@login_required
def accountInfo(request):
    return HttpResponse("501 Not Implemented")


#Send email with credentials when vm is created
def sendMail(request, ssh_user, temp_password):
    current_user = str(request.user)
    data = User.objects.filter(username__exact=current_user)
    for value in data:
        user_email = value.email

    body = '{} \n {}'.format(ssh_user, temp_password)    
    email = EmailMessage('Credentials VMX Virtual Machine', body, to=[user_email])
    email.send()
      
#Generate a random set of chars
def generateRandChar(amount):
    return ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(amount))
          

      