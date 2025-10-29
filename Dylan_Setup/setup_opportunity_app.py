"""
Dylan Brooks
20 October 2025
CSCI 340
Opportunity App Setup Script - Django Version with Accounts
"""

import os
from pathlib import Path
import subprocess
import sys

# --- Project Name ---
PROJECT_NAME = "Dylan_opportunity_app"

# --- 1️⃣ Create Virtual Environment ---
print("🔧 Creating virtual environment...")
subprocess.run([sys.executable, "-m", "venv", "venv"])

# --- 2️⃣ Activate & Install Django ---
print("📦 Installing Django and dependencies...")
pip_path = Path("venv/Scripts/pip") if os.name == "nt" else Path("venv/bin/pip")
subprocess.run([str(pip_path), "install", "django", "psycopg2-binary", "django-crispy-forms"])

# --- 3️⃣ Create Django Project ---
print("📁 Creating Django project...")
django_path = Path("venv/Scripts/python") if os.name == "nt" else Path("venv/bin/python")
subprocess.run([str(django_path), "-m", "django", "startproject", PROJECT_NAME])

# --- 4️⃣ Create Accounts App ---
accounts_app_path = Path(PROJECT_NAME) / "accounts"
subprocess.run([str(django_path), f"{PROJECT_NAME}/manage.py", "startapp", "accounts"])

# --- 5️⃣ Create Folders for Templates ---
(accounts_app_path / "templates/accounts").mkdir(parents=True, exist_ok=True)

# --- 6️⃣ Write models.py (Custom User) ---
(models_path := accounts_app_path / "models.py").write_text("""
from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    ROLE_CHOICES = (
        ('student', 'Student'),
        ('organization', 'Organization'),
    )
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)

    def __str__(self):
        return f"{self.username} ({self.role})"
""")

# --- 7️⃣ Write forms.py ---
(forms_path := accounts_app_path / "forms.py").write_text("""
from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordResetForm
from .models import User

class SignUpForm(UserCreationForm):
    role = forms.ChoiceField(choices=User.ROLE_CHOICES, required=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'role', 'password1', 'password2')

class LoginForm(AuthenticationForm):
    pass

class ForgotPasswordForm(PasswordResetForm):
    pass
""")

# --- 8️⃣ Write views.py ---
(views_path := accounts_app_path / "views.py").write_text("""
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.views import PasswordResetView
from .forms import SignUpForm, LoginForm, ForgotPasswordForm

def signup_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('/')
    else:
        form = SignUpForm()
    return render(request, 'accounts/signup.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('/')
    else:
        form = LoginForm()
    return render(request, 'accounts/login.html', {'form': form})

class CustomPasswordResetView(PasswordResetView):
    template_name = 'accounts/password_reset.html'
""")

# --- 9️⃣ Write urls.py ---
(urls_path := accounts_app_path / "urls.py").write_text("""
from django.urls import path
from .views import signup_view, login_view, CustomPasswordResetView

urlpatterns = [
    path('signup/', signup_view, name='signup'),
    path('login/', login_view, name='login'),
    path('password_reset/', CustomPasswordResetView.as_view(), name='password_reset'),
]
""")

# --- 10️⃣ Write basic templates ---
signup_template = accounts_app_path / "templates/accounts/signup.html"
signup_template.write_text("""
<h2>Sign Up</h2>
<form method="post">
  {% csrf_token %}
  {{ form.as_p }}
  <button type="submit">Sign Up</button>
</form>
<a href="{% url 'login' %}">Login</a>
""")

login_template = accounts_app_path / "templates/accounts/login.html"
login_template.write_text("""
<h2>Login</h2>
<form method="post">
  {% csrf_token %}
  {{ form.as_p }}
  <button type="submit">Login</button>
</form>
<a href="{% url 'signup' %}">Sign Up</a> |
<a href="{% url 'password_reset' %}">Forgot Password?</a>
""")

password_reset_template = accounts_app_path / "templates/accounts/password_reset.html"
password_reset_template.write_text("""
<h2>Forgot Password</h2>
<form method="post">
  {% csrf_token %}
  {{ form.as_p }}
  <button type="submit">Reset Password</button>
</form>
<a href="{% url 'login' %}">Back to Login</a>
""")

# --- 11️⃣ Update project urls.py to include accounts ---
project_urls_path = Path(PROJECT_NAME) / PROJECT_NAME / "urls.py"
project_urls_content = project_urls_path.read_text()
if "include(" not in project_urls_content:
    project_urls_content = project_urls_content.replace(
        "from django.urls import path",
        "from django.urls import path, include"
    )
project_urls_content = project_urls_content.replace(
    "urlpatterns = [",
    "urlpatterns = [\n    path('accounts/', include('accounts.urls')),"
)
project_urls_path.write_text(project_urls_content)

# --- 12️⃣ Instructions for user ---
print("\n✅ Django Opportunity App created with Accounts app!")
print("Next steps:")
print("1. Activate your venv:")
print("   Windows: venv\\Scripts\\activate")
print("   Mac/Linux: source venv/bin/activate")
print("2. Navigate to the project folder:")
print(f"   cd {PROJECT_NAME}")
print("3. Apply migrations:")
print("   python manage.py makemigrations")
print("   python manage.py migrate")
print("4. Create a superuser:")
print("   python manage.py createsuperuser")
print("5. Run the server:")
print("   python manage.py runserver")
print("6. Open your browser:")
print("   http://127.0.0.1:8000/accounts/login/")
print("   http://127.0.0.1:8000/accounts/signup/")
print("   http://127.0.0.1:8000/accounts/password_reset/")
