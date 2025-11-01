from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import StudentProfile

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
def profile_student(request):
    profile, created = StudentProfile.objects.get_or_create(user=request.user)
    experiences = profile.experiences.all()
    context = {
        'profile': profile,
        'experiences': experiences,
    }
    return render(request, 'pages/Profile_STUDENT.html', context)
