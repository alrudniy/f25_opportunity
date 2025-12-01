from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .models import Achievement, Application, Opportunity
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

@login_required
def dashboard(request):
    return render(request, 'pages/dashboard.html')

@login_required
def review_volunteers(request):
    if not hasattr(request.user, 'user_type') or request.user.user_type != 'organization':
        # Redirect non-organizations
        return redirect('screen1')

    if request.method == 'POST':
        application_id = request.POST.get('application_id')
        new_status = request.POST.get('status')
        if application_id and new_status:
            # Check that this application belongs to an opportunity of this organization
            application = Application.objects.filter(
                id=application_id,
                opportunity__organization=request.user
            ).first()
            if application and new_status in Application.ApplicationStatus.values:
                application.status = new_status
                application.save()
                messages.success(request, f"Application status for {application.student.display_name} updated to '{application.get_status_display()}'.")
        return redirect('review_volunteers')


    applications = Application.objects.filter(
        opportunity__organization=request.user
    ).select_related('student', 'opportunity').order_by('-applied_at')
    
    return render(request, 'pages/review_volunteers.html', {
        'applications': applications,
        'status_choices': Application.ApplicationStatus
    })
