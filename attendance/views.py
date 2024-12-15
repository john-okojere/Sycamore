from django.shortcuts import render

def scanner(request):
    return render(request, 'attendance/scanner.html')