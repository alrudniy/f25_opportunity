from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db import models  # Import the models module
from .models import Volunteer, Event, Opportunity

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

def about(request):
    total_volunteers = Volunteer.objects.count()
    total_events = Event.objects.count()
    total_hours = Opportunity.objects.aggregate(models.Sum('total_hours'))['total_hours__sum'] or 0
    
    context = {
        'total_volunteers': total_volunteers,
        'total_events': total_events,
        'total_hours': total_hours,
    }
    return render(request, 'pages/about.html', context)

@login_required
def company_about(request):
    context = {
        'display_name': request.user.display_name,
        'mission': "Our mission is to connect passionate volunteers with meaningful opportunities to make a positive impact in their communities.",
        'problems_solved': "We help address community needs by streamlining volunteer recruitment, event management, and opportunity matching, ensuring efficient resource allocation and greater societal benefit.",
        'contact_email': request.user.email,
    }
    return render(request, 'pages/company_about.html', context)
