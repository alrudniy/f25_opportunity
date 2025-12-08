from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings

from .models import Achievement, Opportunity, Application
from .forms import AchievementForm, OpportunityForm, ApplicationForm

User = get_user_model()

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

# --- Opportunity Related Views ---

@login_required
def create_opportunity(request):
    if request.user.user_type != User.UserType.ORGANIZATION:
        return redirect('screen1') # Or some other appropriate redirect

    if request.method == 'POST':
        form = OpportunityForm(request.POST)
        if form.is_valid():
            opportunity = form.save(commit=False)
            opportunity.organization = request.user
            opportunity.save()
            opportunity.send_new_opportunity_notification() # Send email notification
            return redirect('dashboard') # Or wherever opportunities are listed
    else:
        form = OpportunityForm()

    return render(request, 'pages/create_opportunity.html', {'form': form})

@login_required
def view_opportunities(request):
    # This view would list opportunities, potentially filtered by followed orgs
    opportunities = Opportunity.objects.all().order_by('-created_at')
    return render(request, 'pages/opportunities_list.html', {'opportunities': opportunities})

@login_required
def opportunity_detail(request, pk):
    opportunity = get_object_or_404(Opportunity, pk=pk)
    return render(request, 'pages/opportunity_detail.html', {'opportunity': opportunity})

# --- Application Related Views ---

@login_required
def apply_to_opportunity(request, opportunity_pk):
    if request.user.user_type != User.UserType.STUDENT:
        return redirect('screen1') # Or some other appropriate redirect

    opportunity = get_object_or_404(Opportunity, pk=opportunity_pk)

    if request.method == 'POST':
        form = ApplicationForm(request.POST)
        if form.is_valid():
            application = form.save(commit=False)
            application.student = request.user
            application.opportunity = opportunity
            application.save()
            # Send email for new application submitted
            subject = f"New Application Submitted: {opportunity.title}"
            message = f"A new application has been submitted for the opportunity '{opportunity.title}' by {request.user.display_name}."
            html_message = render_to_string('emails/new_application_submitted.html', {
                'application': application,
                'student_name': request.user.display_name,
                'opportunity_title': opportunity.title,
                'organization_name': opportunity.organization.display_name,
                'base_url': settings.BASE_URL if hasattr(settings, 'BASE_URL') else 'http://localhost:8000',
            })
            # Send to the organization that posted the opportunity
            opportunity.organization.send_email(subject, message, html_message=html_message)
            return redirect('dashboard') # Or wherever applications are listed
    else:
        form = ApplicationForm()

    return render(request, 'pages/apply_opportunity.html', {
        'form': form,
        'opportunity': opportunity,
    })

@login_required
def manage_applications(request):
    # For organizations to view and manage applications
    if request.user.user_type != User.UserType.ORGANIZATION:
        return redirect('screen1')

    # Get opportunities posted by this organization
    opportunities = Opportunity.objects.filter(organization=request.user)
    # Get all applications for these opportunities
    applications = Application.objects.filter(opportunity__in=opportunities).order_by('-applied_at')

    if request.method == 'POST':
        app_id = request.POST.get('application_id')
        new_status = request.POST.get('status')
        if app_id and new_status:
            application = get_object_or_404(Application, pk=app_id)
            if application.opportunity.organization == request.user: # Ensure it's their application
                application.status = new_status
                application.save() # This will trigger the email in the model's save method
                # If you want to send a reminder email specifically here, you would add that logic.
                # For now, the status change email is handled by the model.
                return redirect('manage_applications')

    return render(request, 'pages/manage_applications.html', {
        'applications': applications,
        'opportunities': opportunities,
    })

# Placeholder for sending reminder emails
def send_application_reminder(request, application_pk):
    application = get_object_or_404(Application, pk=application_pk)
    if request.user == application.student or request.user == application.opportunity.organization:
        subject = f"Reminder: Application for {application.opportunity.title}"
        message = f"This is a reminder about your application for '{application.opportunity.title}'. Current status: {application.get_status_display()}."
        html_message = render_to_string('emails/application_reminder.html', {
            'application': application,
            'student_name': application.student.display_name,
            'opportunity_title': application.opportunity.title,
            'current_status': application.get_status_display(),
            'base_url': settings.BASE_URL if hasattr(settings, 'BASE_URL') else 'http://localhost:8000',
        })
        application.student.send_email(subject, message, html_message=html_message)
        # Optionally, send a reminder to the organization as well
        # application.opportunity.organization.send_email(subject, message, html_message=html_message)
        return redirect('dashboard') # Or wherever appropriate
    else:
        return redirect('screen1') # Unauthorized

# --- Chat Related Views ---
# Assuming a basic chat structure where messages are sent and received.
# You'll need to implement the actual chat view logic separately.

# Example of how you might trigger a chat reply notification
# This would typically be called after a message is successfully saved.
def send_chat_reply_notification(message):
    """Triggers the email notification for a new chat reply."""
    message.send_new_reply_notification()

