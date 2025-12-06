from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from .models import Achievement, FindOpportunity
from .forms import AchievementForm


def welcome(request):
    return render(request, 'pages/welcome.html')

@login_required
def screen1(request):
    role = request.user.user_type.title() if hasattr(request.user, 'user_type') else 'User'
    
    # Start with all published opportunities
    opportunities = FindOpportunity.objects.filter(status='published')
    
    # Apply filters from GET parameters
    opportunity_type = request.GET.get('opportunity_type')
    if opportunity_type:
        opportunities = opportunities.filter(opportunity_type=opportunity_type)
    
    location_type = request.GET.get('location_type')
    if location_type == 'remote':
        opportunities = opportunities.filter(is_remote=True)
    elif location_type == 'in_person':
        opportunities = opportunities.filter(is_remote=False)
    
    city = request.GET.get('city')
    if city:
        opportunities = opportunities.filter(city=city)
    
    state = request.GET.get('state')
    if state:
        opportunities = opportunities.filter(state=state)
    
    search_query = request.GET.get('search_query')
    if search_query:
        opportunities = opportunities.filter(title__icontains=search_query)
    
    # Get total count
    total_count = opportunities.count()
    
    return render(request, 'pages/screen1.html', {
        'role': role,
        'opportunities': opportunities,
        'total_count': total_count,
    })

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
