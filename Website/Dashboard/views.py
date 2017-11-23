from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth.decorators import login_required

from . import forms
from VMManager.views import createNewVM

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

        if form.is_valid():
            createNewVM(
                request,
                form.cleaned_data["VirtualMachineName"],
                form.cleaned_data["CPUCores"],
                form.cleaned_data["RAMAmount"],
                form.cleaned_data["DiskSize"]
            )
        
        return redirect("/dashboard/")

<<<<<<< HEAD

    
=======
@login_required
def start_VM(request):
    return HttpResponse('Vm is gestart!')
>>>>>>> master

@login_required
def accountInfo(request):
    return HttpResponse("501 Not Implemented")
      

      