from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import StudentProfile
from .forms import ExperienceForm, StudentProfileForm

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

@login_required
def add_experience(request):
    # Ensure the user has a student profile
    if not hasattr(request.user, 'student_profile'):
        # Or redirect to a profile creation page if you have one
        return redirect('profile_student')

    profile = request.user.student_profile
    if request.method == 'POST':
        form = ExperienceForm(request.POST)
        if form.is_valid():
            experience = form.save(commit=False)
            experience.profile = profile
            experience.save()
            return redirect('profile_student')
    else:
        form = ExperienceForm()
    
    context = {
        'form': form,
        'title': 'Add Experience'
    }
    return render(request, 'pages/experience_form.html', context)

@login_required
def edit_profile_student(request):
    profile, created = StudentProfile.objects.get_or_create(user=request.user)
    if request.method == 'POST':
        form = StudentProfileForm(request.POST, request.FILES, instance=profile, user=request.user)
        if form.is_valid():
            form.save()
            return redirect('profile_student')
    else:
        form = StudentProfileForm(instance=profile, user=request.user)
    
    context = {
        'form': form,
        'title': 'Edit Profile'
    }
    return render(request, 'pages/experience_form.html', context)
