from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model

from .models import Achievement, OrganizationSubscription
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
    if hasattr(request.user, 'user_type') and request.user.user_type == 'student':
        User = get_user_model()
        organizations = User.objects.filter(user_type='organization')

        subscriptions = OrganizationSubscription.objects.filter(student=request.user).values_list('organization_id', flat=True)

        organizations_with_status = []
        for org in organizations:
            organizations_with_status.append({
                'organization': org,
                'is_following': org.id in subscriptions
            })

        return render(request, 'pages/dashboard.html', {'organizations': organizations_with_status})

    return render(request, 'pages/dashboard.html')


@login_required
def follow_organization(request, organization_id):
    if request.method == 'POST':
        if not hasattr(request.user, 'user_type') or request.user.user_type != 'student':
            return redirect('screen1')

        User = get_user_model()
        organization = get_object_or_404(User, id=organization_id, user_type='organization')

        OrganizationSubscription.objects.get_or_create(student=request.user, organization=organization)
    return redirect('dashboard')


@login_required
def unfollow_organization(request, organization_id):
    if request.method == 'POST':
        if not hasattr(request.user, 'user_type') or request.user.user_type != 'student':
            return redirect('screen1')

        User = get_user_model()
        organization = get_object_or_404(User, id=organization_id, user_type='organization')

        OrganizationSubscription.objects.filter(student=request.user, organization=organization).delete()
    return redirect('dashboard')
