from django.shortcuts import render


def homepage(request):
    return render(request, 'index.html')


def giveOnline(request):
    return render(request, 'give.html')

def register(request):
    return render(request, 'register.html')