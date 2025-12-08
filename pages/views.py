from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

def welcome(request):
    return render(request, 'pages/welcome.html')

@login_required
def screen1(request):
    return render(request, 'pages/screen1.html')

@login_required
def screen2(request):
    return render(request, 'pages/screen2.html')

@login_required
def screen3(request):
    return render(request, 'pages/screen3.html')

@login_required
def company_about(request):
    if request.user.user_type != 'organization':
        return redirect('screen1')
    return render(request, 'pages/company_about.html')
