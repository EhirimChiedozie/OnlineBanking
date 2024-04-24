from django.shortcuts import render

# Create your views here.

def home(request):
    return render(request, 'bankapp/home.html')

def about(request):
    welcome_address = 'Welcome to the about page of my bank site'
    context = {'welcome_address':welcome_address}
    return render(request, 'bankapp/about.html', context=context)