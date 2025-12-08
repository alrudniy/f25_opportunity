from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.test import TestCase, Client
from django.urls import reverse

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

# --- Tests ---
class CompanyAboutAccessControlTest(TestCase):
    def setUp(self):
        self.client = Client()
        # Create a dummy user that is not an organization
        from django.contrib.auth import get_user_model
        User = get_user_model()
        self.student_user = User.objects.create_user(username='student', password='password', user_type='student')
        self.organization_user = User.objects.create_user(username='organization', password='password', user_type='organization')

    def test_company_about_redirects_non_company_users(self):
        """
        Verify that non-company users are redirected from company_about page.
        """
        # Test with a student user
        self.client.login(username='student', password='password')
        response = self.client.get(reverse('company_about'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('screen1'))

        # Test with a user that has no user_type (should also be redirected)
        # For simplicity, we'll assume the default user creation doesn't set user_type
        # If your User model has a default, this test might need adjustment.
        # For now, we'll rely on the student_user test which covers a non-organization type.

    def test_company_about_allows_company_users(self):
        """
        Verify that company users can access the company_about page.
        """
        self.client.login(username='organization', password='password')
        response = self.client.get(reverse('company_about'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'pages/company_about.html')
