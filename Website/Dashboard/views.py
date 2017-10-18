from django.shortcuts import render, HttpResponse, redirect

from . import forms
from VMManager.views import createNewVM

# Create your views here.
def index(request):
    if request.user.is_authenticated():
        return render(request, 'home/home.html')
    else:
        return redirect('/login')

def myVM(request):
    return HttpResponse("501 Not Implemented")

def createVM(request):
    if request.user.is_authenticated():
        if request.method == "GET":
            form = forms.NewVMForm()
            return render(request, "home/CreateVM.html", {'form': form})
        elif request.method == "POST":
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


    

def accountInfo(request):
    return HttpResponse("501 Not Implemented")
      

      