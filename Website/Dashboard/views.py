from django.shortcuts import render, HttpResponse, redirect

# Create your views here.
def index(request):
    if request.user.is_authenticated():
        return render(request, 'home/dashboard.html')
    else:
        return redirect('/login')


      