from django.shortcuts import render

# Create your views here.

def esports(request):
    return render(request, 'esports.html')

def bgmi(request):
    return render(request, 'bgmi.html')

def valorant(request):
    return render(request, 'valorant.html')

def cod_m(request):
    return render(request, 'codm.html')

def content_creation(request):
    return render(request, 'content_creation.html')
