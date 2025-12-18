from django.shortcuts import render


def report_page(request):
    return render(request, 'report.html', {})

def login_page(request):
    return render(request, 'login.html')

def home_page(request):
    return render(request, 'homepage.html', {})
