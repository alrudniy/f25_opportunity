from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.conf import settings

from .models import Achievement
from .forms import AchievementForm

def welcome(request):
    return render(request, 'pages/welcome.html')

@login_required
def screen1(request):
    role = request.user.user_type.title() if hasattr(request.user, 'user_type') else 'User'
    return render(request, 'pages/screen1.html', {'role': role})

@login_required
def screen2(request):
    role = request.user.user_type.title() if hasattr(request.user, 'user_type') else 'User'
    return render(request, 'pages/screen2.html', {'role': role})

@login_required
def screen3(request):
    role = request.user.user_type.title() if hasattr(request.user, 'user_type') else 'User'
    return render(request, 'pages/screen3.html', {'role': role})


@login_required
def student_achievements(request):
    if not hasattr(request.user, 'user_type') or request.user.user_type != 'student':
        # Redirect non-students
        return redirect('screen1')

    if request.method == 'POST':
        form = AchievementForm(request.POST)
        if form.is_valid():
            achievement = form.save(commit=False)
            achievement.student = request.user
            achievement.save()
            return redirect('student_achievements')
    else:
        form = AchievementForm()

    achievements = Achievement.objects.filter(student=request.user).order_by('-date_completed')
    return render(request, 'pages/student_achievements.html', {
        'achievements': achievements,
        'form': form,
    })

def faq(request):
    return render(request, 'pages/faq.html')

def dashboard(request):
    return render(request, 'pages/dashboard.html')

@login_required
def company_about(request):
    # Assuming the logged-in user is an organization
    company_display_name = request.user.display_name
    mission_text = "Our mission is to connect students with meaningful opportunities and foster growth."
    problems_solved = "We help organizations find talented students for internships and projects, while providing students with valuable real-world experience."
    contact_email = "info@opportunityapp.com" # Replace with actual contact email if available

    return render(request, 'pages/company_about.html', {
        'company_display_name': company_display_name,
        'mission_text': mission_text,
        'problems_solved': problems_solved,
        'contact_email': contact_email,
    })
