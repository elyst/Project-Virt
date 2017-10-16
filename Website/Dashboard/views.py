from django.shortcuts import render, HttpResponse, redirect

# Create your views here.
def index(request):
    if request.user.is_authenticated():
        return render(request, 'home/dashboard.html')
    else:
        return redirect('/login')

def myVM(request):
    return HttpResponse("501 Not Implemented")

def createVM(request):
    return HttpResponse("501 Not Implemented")

def accountInfo(request):
    return HttpResponse("501 Not Implemented")
      