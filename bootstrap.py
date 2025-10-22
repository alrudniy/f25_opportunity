#!/usr/bin/env python3
"""
One-shot Python bootstrap for the Opportunity App Django project.

What it does:
- Creates a Python venv and installs: Django, psycopg2-binary, python-dotenv
- Creates Django project + two apps: accounts, pages
- Configures Postgres (34.16.174.60 / oppo_app / CSCI340Fall2025) via .env
- Implements custom User model with user_type (student, organization, administrator) and email login
- Adds Login + Create Account screens
- Adds Screen 1 ("Hello {User's Name}") with buttons to Screen 2 and Screen 3, and simple navigation
- Creates minimal templates and CSS

Usage:
    python bootstrap.py

Notes:
- If the remote DB is unreachable during migration, you'll see a helpful message.
- Re-run migrations later with: source .venv/bin/activate && python manage.py migrate
"""
import os
import sys
import platform
import subprocess
from pathlib import Path
from textwrap import dedent

PROJECT = "opportunity_app"  # Django settings package name
VENV_DIR = Path(".venv")

def is_windows() -> bool:
    return os.name == "nt" or platform.system().lower().startswith("win")

def venv_python() -> Path:
    if is_windows():
        return VENV_DIR / "Scripts" / "python.exe"
    return VENV_DIR / "bin" / "python"

def run(cmd, cwd=None, env=None, check=True):
    print(f">> {' '.join(str(c) for c in cmd)}")
    return subprocess.run(cmd, cwd=cwd, env=env, check=check)

def write(path: Path, content: str):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")
    print(f"   wrote {path}")

def main():
    cwd = Path.cwd()
    print(f"== Bootstrap in {cwd}")

    # 1) Create venv
    if not VENV_DIR.exists():
        print(">> Creating virtualenv")
        run([sys.executable, "-m", "venv", str(VENV_DIR)])
    else:
        print(">> Virtualenv exists; continuing")

    py = venv_python()
    if not py.exists():
        print("!! Could not find interpreter in venv:", py)
        sys.exit(1)

    # 2) Install dependencies
    print(">> Upgrading pip / installing dependencies")
    run([str(py), "-m", "pip", "install", "--upgrade", "pip"])
    run([str(py), "-m", "pip", "install", "Django>=5.0,<6.0", "psycopg2-binary", "python-dotenv"])

    # 3) Start Django project (if not present)
    if not (cwd / "manage.py").exists():
        print(">> Creating Django project")
        run([str(py), "-m", "django", "startproject", PROJECT, "."])
    else:
        print(">> manage.py exists; skipping startproject")

    # 4) Create apps
    if not (cwd / "accounts").exists():
        print(">> Creating 'accounts' app")
        run([str(py), "manage.py", "startapp", "accounts"])
    else:
        print(">> 'accounts' app exists; skipping")

    if not (cwd / "pages").exists():
        print(">> Creating 'pages' app")
        run([str(py), "manage.py", "startapp", "pages"])
    else:
        print(">> 'pages' app exists; skipping")

    # 5) .env with DB settings
    write(cwd / ".env", dedent("""\
        DJANGO_SECRET_KEY=dev-insecure-change-me
        DJANGO_DEBUG=True
        DB_NAME=opportunity_db
        DB_USER=oppo_app
        DB_PASSWORD=CSCI340Fall2025
        DB_HOST=34.16.174.60
        DB_PORT=5432
        ALLOWED_HOSTS=127.0.0.1,localhost
    """))

    # 6) settings.py
    settings_py = dedent(f"""\
        from pathlib import Path
        import os
        from dotenv import load_dotenv

        BASE_DIR = Path(__file__).resolve().parent.parent
        load_dotenv(BASE_DIR / '.env')

        SECRET_KEY = os.getenv('DJANGO_SECRET_KEY', 'dev-insecure-change-me')
        DEBUG = os.getenv('DJANGO_DEBUG', 'True').lower() == 'true'
        ALLOWED_HOSTS = [h.strip() for h in os.getenv('ALLOWED_HOSTS', '127.0.0.1,localhost').split(',') if h.strip()]

        INSTALLED_APPS = [
            'django.contrib.admin','django.contrib.auth','django.contrib.contenttypes',
            'django.contrib.sessions','django.contrib.messages','django.contrib.staticfiles',
            'accounts','pages',
        ]

        MIDDLEWARE = [
            'django.middleware.security.SecurityMiddleware',
            'django.contrib.sessions.middleware.SessionMiddleware',
            'django.middleware.common.CommonMiddleware',
            'django.middleware.csrf.CsrfViewMiddleware',
            'django.contrib.auth.middleware.AuthenticationMiddleware',
            'django.contrib.messages.middleware.MessageMiddleware',
            'django.middleware.clickjacking.XFrameOptionsMiddleware',
        ]

        ROOT_URLCONF = '{PROJECT}.urls'
        TEMPLATES = [{{
            'BACKEND':'django.template.backends.django.DjangoTemplates',
            'DIRS':[BASE_DIR/'templates'],
            'APP_DIRS':True,
            'OPTIONS':{{
                'context_processors':[
                    'django.template.context_processors.debug',
                    'django.template.context_processors.request',
                    'django.contrib.auth.context_processors.auth',
                    'django.contrib.messages.context_processors.messages',
                ],
            }},
        }}]
        WSGI_APPLICATION = '{PROJECT}.wsgi.application'

        DATABASES = {{
            'default': {{
                'ENGINE': 'django.db.backends.postgresql',
                'NAME': os.getenv('DB_NAME','opportunity_db'),
                'USER': os.getenv('DB_USER','oppo_app'),
                'PASSWORD': os.getenv('DB_PASSWORD','CSCI340Fall2025'),
                'HOST': os.getenv('DB_HOST','34.16.174.60'),
                'PORT': int(os.getenv('DB_PORT','5432')),
                'CONN_MAX_AGE': 60,
            }}
        }}

        AUTH_USER_MODEL = 'accounts.User'

        AUTH_PASSWORD_VALIDATORS = [
            {{'NAME':'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'}},
            {{'NAME':'django.contrib.auth.password_validation.MinimumLengthValidator','OPTIONS':{{'min_length':8}}}},
            {{'NAME':'django.contrib.auth.password_validation.CommonPasswordValidator'}},
            {{'NAME':'django.contrib.auth.password_validation.NumericPasswordValidator'}},
        ]

        LANGUAGE_CODE = 'en-us'
        TIME_ZONE = 'UTC'
        USE_I18N = True
        USE_TZ = True

        STATIC_URL = '/static/'
        STATICFILES_DIRS = [BASE_DIR / 'static']

        DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

        LOGIN_URL = 'login'
        LOGIN_REDIRECT_URL = 'screen1'
        LOGOUT_REDIRECT_URL = 'login'
    """)
    write(cwd / PROJECT / "settings.py", settings_py)

    # 7) root urls.py
    urls_root = dedent("""\
        from django.contrib import admin
        from django.urls import path, include

        urlpatterns = [
            path('admin/', admin.site.urls),
            path('', include('pages.urls')),
            path('accounts/', include('accounts.urls')),
        ]
    """)
    write(cwd / PROJECT / "urls.py", urls_root)

    # 8) accounts app files
    accounts_models = dedent("""\
        from django.contrib.auth.models import AbstractUser
        from django.db import models

        class User(AbstractUser):
            class UserType(models.TextChoices):
                STUDENT = 'student', 'Student'
                ORGANIZATION = 'organization', 'Organization'
                ADMINISTRATOR = 'administrator', 'Administrator'

            user_type = models.CharField(max_length=20, choices=UserType.choices, default=UserType.STUDENT)
            email = models.EmailField(unique=True)

            USERNAME_FIELD = 'email'
            REQUIRED_FIELDS = ['username']  # keep username for admin compatibility

            def save(self, *args, **kwargs):
                if not self.username:
                    self.username = self.email
                super().save(*args, **kwargs)

            @property
            def display_name(self):
                full = f"{self.first_name} {self.last_name}".strip()
                return full if full else self.email
    """)
    write(cwd / "accounts" / "models.py", accounts_models)

    accounts_forms = dedent("""\
        from django import forms
        from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
        from .models import User

        class UserRegistrationForm(UserCreationForm):
            user_type = forms.ChoiceField(choices=User.UserType.choices, widget=forms.RadioSelect)

            class Meta:
                model = User
                fields = ('email', 'password1', 'password2', 'user_type')

        class EmailAuthenticationForm(AuthenticationForm):
            # Field is still named "username" internally; label it clearly as Email.
            def __init__(self, *args, **kwargs):
                super().__init__(*args, **kwargs)
                self.fields['username'].label = 'Email'
                self.fields['username'].widget.attrs.update({'placeholder': 'you@example.com', 'autofocus': True})
                self.fields['password'].widget.attrs.update({'placeholder': 'password'})
    """)
    write(cwd / "accounts" / "forms.py", accounts_forms)

    accounts_views = dedent("""\
        from django.contrib.auth import login as auth_login
        from django.contrib.auth.views import LoginView
        from django.urls import reverse_lazy
        from django.views.generic import FormView
        from .forms import UserRegistrationForm, EmailAuthenticationForm

        class RegisterView(FormView):
            template_name = 'accounts/register.html'
            form_class = UserRegistrationForm
            success_url = reverse_lazy('screen1')

            def form_valid(self, form):
                user = form.save()
                auth_login(self.request, user)
                return super().form_valid(form)

            def get_initial(self):
                initial = super().get_initial()
                user_type = self.request.GET.get('type') or self.request.session.get('selected_user_type')
                if user_type:
                    initial['user_type'] = user_type
                return initial

        class CustomLoginView(LoginView):
            template_name = 'accounts/login.html'
            authentication_form = EmailAuthenticationForm
            redirect_authenticated_user = True

            def get_success_url(self):
                return reverse_lazy('screen1')

            def get_context_data(self, **kwargs):
                context = super().get_context_data(**kwargs)
                user_type = self.request.GET.get('type')
                if user_type:
                    self.request.session['selected_user_type'] = user_type
                context['selected_user_type'] = user_type
                return context
    """)
    write(cwd / "accounts" / "views.py", accounts_views)

    accounts_urls = dedent("""\
        from django.urls import path
        from django.contrib.auth.views import LogoutView
        from .views import RegisterView, CustomLoginView

        urlpatterns = [
            path('login/', CustomLoginView.as_view(), name='login'),
            path('register/', RegisterView.as_view(), name='register'),
            path('logout/', LogoutView.as_view(), name='logout'),
        ]
    """)
    write(cwd / "accounts" / "urls.py", accounts_urls)

    accounts_admin = dedent("""\
        from django.contrib import admin
        from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
        from django.utils.translation import gettext_lazy as _
        from .models import User

        @admin.register(User)
        class UserAdmin(BaseUserAdmin):
            fieldsets = (
                (None, {'fields': ('email', 'password')}),
                (_('Personal info'), {'fields': ('first_name', 'last_name')}),
                (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
                (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
                (_('Meta'), {'fields': ('user_type', 'username')}),
            )
            add_fieldsets = (
                (None, {'classes': ('wide',), 'fields': ('email', 'password1', 'password2', 'user_type')}),
            )
            list_display = ('email', 'user_type', 'is_staff', 'is_active')
            search_fields = ('email', 'first_name', 'last_name')
            ordering = ('email',)
    """)
    write(cwd / "accounts" / "admin.py", accounts_admin)

    # 9) pages app files
    pages_views = dedent("""\
        from django.shortcuts import render
        from django.contrib.auth.decorators import login_required

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
    """)
    write(cwd / "pages" / "views.py", pages_views)

    pages_urls = dedent("""\
        from django.urls import path
        from . import views

        urlpatterns = [
            path('', views.welcome, name='welcome'),
            path('screen1/', views.screen1, name='screen1'),
            path('screen2/', views.screen2, name='screen2'),
            path('screen3/', views.screen3, name='screen3'),
        ]
    """)
    write(cwd / "pages" / "urls.py", pages_urls)

    # 10) templates & static
    write(cwd / "static" / "css" / "styles.css", dedent("""\
        * { box-sizing: border-box; }
        body { margin:0; font-family: system-ui, -apple-system, Segoe UI, Roboto, Arial, sans-serif; background:#f7f7fb; color:#111; }
        .container { max-width: 960px; margin: 0 auto; padding: 1.25rem; }
        .site-header { background:#fff; border-bottom:1px solid #e5e7eb; position: sticky; top:0; }
        .header-inner { display:flex; align-items:center; justify-content:space-between; }
        .brand { font-weight:700; text-decoration:none; color:#111; }
        .nav { list-style:none; display:flex; gap:.75rem; margin:0; padding:0; align-items:center; }
        .nav .divider { width:1px; background:#e5e7eb; height:22px; margin:0 .5rem; }
        .nav a { text-decoration:none; color:#0f172a; padding:.4rem .6rem; border-radius:.4rem; }
        .nav a:hover { background:#f1f5f9; }
        .nav .muted { color:#475569; padding:.4rem .6rem; }
        .site-footer { margin-top:3rem; padding:1rem 0; color:#6b7280; }
        .auth-card, .dash-card { background:#fff; border:1px solid #e5e7eb; border-radius:.8rem; padding:2rem; margin-top:2rem; }
        h1 { margin-top:0; }
        .form-field { margin-bottom:1rem; display:flex; flex-direction:column; }
        .form-field input[type="text"], .form-field input[type="email"], .form-field input[type="password"] { padding:.6rem .7rem; border:1px solid #cbd5e1; border-radius:.5rem; }
        fieldset.form-field { border:1px solid #e5e7eb; border-radius:.6rem; padding:.75rem 1rem; }
        .button-row { display:flex; gap:.75rem; flex-wrap:wrap; margin-top:1rem; }
        .btn { display:inline-block; background:#111827; color:#fff; text-decoration:none; padding:.6rem .9rem; border-radius:.6rem; }
        .btn.primary { background:#2563eb; }
        .btn:hover { filter:brightness(1.05); }
        .muted { color:#64748b; }
        .error { color:#b91c1c; font-size:.9rem; margin-top:.25rem; }
        .messages { list-style:none; padding:0; }
        .messages li { background:#ecfeff; border:1px solid #22d3ee; color:#0e7490; padding:.6rem .9rem; border-radius:.5rem; margin:.5rem 0; }
    """))

    base_html = dedent("""\
        {% load static %}
        <!doctype html>
        <html lang="en">
        <head>
          <meta charset="utf-8"/>
          <title>Opportunity App</title>
          <meta name="viewport" content="width=device-width, initial-scale=1"/>
          <link rel="stylesheet" href="{% static 'css/styles.css' %}">
        </head>
        <body>
          <header class="site-header">
            <div class="container header-inner">
              <a class="brand" href="{% url 'welcome' %}">Opportunity App</a>
              <nav>
                <ul class="nav">
                  {% if user.is_authenticated %}
                    <li><a href="{% url 'screen1' %}">Screen 1</a></li>
                    <li><a href="{% url 'screen2' %}">Screen 2</a></li>
                    <li><a href="{% url 'screen3' %}">Screen 3</a></li>
                    <li class="divider"></li>
                    <li class="muted">Hi, {{ user.display_name }}</li>
                    <li><a href="{% url 'logout' %}">Log out</a></li>
                  {% else %}
                    <li><a href="{% url 'login' %}">Log in</a></li>
                    <li><a href="{% url 'register' %}">Create account</a></li>
                  {% endif %}
                </ul>
              </nav>
            </div>
          </header>

          <main class="container">
            {% if messages %}
              <ul class="messages">
                {% for message in messages %}
                  <li class="{{ message.tags }}">{{ message }}</li>
                {% endfor %}
              </ul>
            {% endif %}
            {% block content %}{% endblock %}
          </main>

          <footer class="site-footer">
            <div class="container">
              <small>&copy; {% now "Y" %} Opportunity App</small>
            </div>
          </footer>
        </body>
        </html>
    """)
    write(cwd / "templates" / "base.html", base_html)

    welcome_html = dedent("""\
        {% extends "base.html" %}
        {% block content %}
          <section class="auth-card">
            <h1>Welcome</h1>
            <p>Please choose your user type to continue.</p>
            <div class="button-row">
              <a class="btn" href="{% url 'login' %}?type=student">I am a Student</a>
              <a class="btn" href="{% url 'login' %}?type=organization">I am an Organization</a>
              <a class="btn" href="{% url 'login' %}?type=administrator">I am an Administrator</a>
            </div>
            <p class="muted">No account? <a href="{% url 'register' %}">Create one</a>.</p>
          </section>
        {% endblock %}
    """)
    write(cwd / "templates" / "pages" / "welcome.html", welcome_html)

    login_html = dedent("""\
        {% extends "base.html" %}
        {% block content %}
          <section class="auth-card">
            <h1>Sign in{% if selected_user_type %} as {{ selected_user_type|title }}{% endif %}</h1>
            <form method="post" novalidate>
              {% csrf_token %}
              <div class="form-field">
                <label for="{{ form.username.id_for_label }}">{{ form.username.label }}</label>
                {{ form.username }}
                {% if form.username.errors %}<div class="error">{{ form.username.errors.0 }}</div>{% endif %}
              </div>
              <div class="form-field">
                <label for="{{ form.password.id_for_label }}">{{ form.password.label }}</label>
                {{ form.password }}
                {% if form.password.errors %}<div class="error">{{ form.password.errors.0 }}</div>{% endif %}
              </div>
              <button class="btn primary" type="submit">Sign in</button>
            </form>
            <div class="auth-links">
              <a href="{% url 'register' %}{% if selected_user_type %}?type={{ selected_user_type }}{% endif %}">Create account</a>
            </div>
          </section>
        {% endblock %}
    """)
    write(cwd / "templates" / "accounts" / "login.html", login_html)

    register_html = dedent("""\
        {% extends "base.html" %}
        {% block content %}
          <section class="auth-card">
            <h1>Create Account</h1>
            <form method="post" novalidate>
              {% csrf_token %}
              <div class="form-field">
                <label for="{{ form.email.id_for_label }}">Email</label>
                {{ form.email }}
                {% if form.email.errors %}<div class="error">{{ form.email.errors.0 }}</div>{% endif %}
              </div>

              <fieldset class="form-field">
                <legend>User type</legend>
                {{ form.user_type }}
                {% if form.user_type.errors %}<div class="error">{{ form.user_type.errors.0 }}</div>{% endif %}
              </fieldset>

              <div class="form-field">
                <label for="{{ form.password1.id_for_label }}">Password</label>
                {{ form.password1 }}
                {% if form.password1.errors %}<div class="error">{{ form.password1.errors.0 }}</div>{% endif %}
              </div>
              <div class="form-field">
                <label for="{{ form.password2.id_for_label }}">Confirm Password</label>
                {{ form.password2 }}
                {% if form.password2.errors %}<div class="error">{{ form.password2.errors.0 }}</div>{% endif %}
              </div>

              <button class="btn primary" type="submit">Create Account</button>
            </form>
            <div class="auth-links">
              <a href="{% url 'login' %}">Back to sign in</a>
            </div>
          </section>
        {% endblock %}
    """)
    write(cwd / "templates" / "accounts" / "register.html", register_html)

    screen1_html = dedent("""\
        {% extends "base.html" %}
        {% block content %}
          <section class="dash-card">
            <h1>Hello {{ request.user.display_name }}</h1>
            <p class="muted">You are signed in as <strong>{{ request.user.user_type|title }}</strong>.</p>
            <div class="button-row">
              <a class="btn" href="{% url 'screen2' %}">Go to Screen 2</a>
              <a class="btn" href="{% url 'screen3' %}">Go to Screen 3</a>
            </div>
          </section>
        {% endblock %}
    """)
    write(cwd / "templates" / "pages" / "screen1.html", screen1_html)

    screen2_html = dedent("""\
        {% extends "base.html" %}
        {% block content %}
          <section class="dash-card">
            <h1>Screen 2</h1>
            <p>This is a placeholder page you can expand later.</p>
            <div><a class="btn" href="{% url 'screen1' %}">← Back to Screen 1</a></div>
          </section>
        {% endblock %}
    """)
    write(cwd / "templates" / "pages" / "screen2.html", screen2_html)

    screen3_html = dedent("""\
        {% extends "base.html" %}
        {% block content %}
          <section class="dash-card">
            <h1>Screen 3</h1>
            <p>This is a placeholder page you can expand later.</p>
            <div><a class="btn" href="{% url 'screen1' %}">← Back to Screen 1</a></div>
          </section>
        {% endblock %}
    """)
    write(cwd / "templates" / "pages" / "screen3.html", screen3_html)

    # 11) Make migrations and migrate
    print(">> makemigrations (accounts)")
    run([str(py), "manage.py", "makemigrations", "accounts"])

    print(">> migrate")
    try:
        run([str(py), "manage.py", "migrate"])
    except subprocess.CalledProcessError:
        print("!! Migration could not connect to the DB.")
        print("   Ensure Postgres at 34.16.174.60:5432 is reachable and credentials are correct, then run:")
        if is_windows():
            print("   .venv\\Scripts\\python manage.py migrate")
        else:
            print("   source .venv/bin/activate && python manage.py migrate")

    print("\n>> All set.")
    if is_windows():
        print("   Start server: .venv\\Scripts\\python manage.py runserver")
    else:
        print("   Start server: source .venv/bin/activate && python manage.py runserver")

if __name__ == "__main__":
    main()
