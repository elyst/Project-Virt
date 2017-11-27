from django.shortcuts import render

# Create your views here.
def index(request):
    return render(request, 'LandingPage/index.html')

def contact(request):
    return render(request, 'LandingPage/page2.html')

def pricing(request):
    return render(request, 'LandingPage/page1.html')

