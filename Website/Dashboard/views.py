from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

from django.core.exceptions import ObjectDoesNotExist

from . import forms
from VMManager.views import createNewVM

from .models import UserInfo

# Create your views here.
@login_required
def index(request):
    return render(request, 'Dashboard/Index.html')

@login_required
def myVM(request):
    return start_VM(request)

@login_required
def createVM(request):
    if request.method == "GET":
        # Generate form and show CreateVM to the user
        form = forms.NewVMForm()
        return render(request, "Dashboard/CreateVM.html", {'form': form})
    elif request.method == "POST":
        # Populate, verify and process the input data
        form = forms.NewVMForm(request.POST)

        if form.is_valid():
            createNewVM(
                request,
                form.cleaned_data["VirtualMachineName"],
                form.cleaned_data["CPUCores"],
                form.cleaned_data["RAMAmount"],
                form.cleaned_data["DiskSize"]
            )
        
        return redirect("/dashboard/")

@login_required
def start_VM(request):
    return HttpResponse('Vm is gestart!')

@login_required
def accountInfo(request):
    # Try to retrieve user info, if failed: create UserInfo 
    try:
        userinf = UserInfo.objects.get(user = request.user)
    except ObjectDoesNotExist:
        userinf = UserInfo()
        userinf.user = User.objects.get(pk=request.user.id)
        userinf.save()

    return render(request, "Dashboard/AccountInfo.html", {
        "user": userinf
    })

@login_required
def editAccountInfo(request):

    return render (request, "Dashboard/EditAccountInfo.html", {
        "form": "hey"
    })