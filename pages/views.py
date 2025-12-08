from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

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
    if not hasattr(request.user, 'user_type') or request.user.user_type != 'organization':
        # Redirect non-organization users, e.g., to their respective dashboards or screen1
        return redirect('screen1') 

    context = {
        'company_name': request.user.display_name if hasattr(request.user, 'display_name') else request.user.username,
        'mission_text': "Our mission is to connect talented individuals with meaningful opportunities to foster professional growth and innovation.",
        'problems_solved_text': "We help companies find the right talent quickly and efficiently, reducing recruitment costs and time-to-hire. For individuals, we provide a platform to discover opportunities aligned with their skills and career aspirations.",
        'contact_email': request.user.email,
    }
    return render(request, 'pages/company_about.html', context)
