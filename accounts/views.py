from django.contrib.auth import login as auth_login, get_user_model
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy
from django.views.generic import FormView
from django.shortcuts import redirect, render
from django.template.loader import render_to_string  # Import render_to_string
from django.conf import settings  # Import settings
from .forms import UserRegistrationForm, EmailAuthenticationForm

User = get_user_model()

class RegisterView(FormView):
    template_name = 'accounts/register.html'
    form_class = UserRegistrationForm
    success_url = reverse_lazy('screen1')

    def form_valid(self, form):
        user = form.save()
        auth_login(self.request, user)
        # Send email for new user registration
        subject = "Welcome to Opportunity App!"
        message = f"Hello {user.display_name},\n\nWelcome to Opportunity App! We're excited to have you on board."
        html_message = render_to_string('emails/welcome_email.html', {
            'user_name': user.display_name,
            'base_url': settings.BASE_URL if hasattr(settings, 'BASE_URL') else 'http://localhost:8000',
        })
        user.send_email(subject, message, html_message=html_message)
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
        # Check if a user type was selected during login and redirect accordingly
        user_type = self.request.session.get('selected_user_type')
        if user_type:
            # You might want to redirect to different initial screens based on user type
            # For now, we'll stick to the general screen1
            return reverse_lazy('screen1')
        return reverse_lazy('screen1') # Default redirect

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_type = self.request.GET.get('type')
        if user_type:
            self.request.session['selected_user_type'] = user_type
        context['selected_user_type'] = user_type
        return context

class CustomLogoutView(LogoutView):
    next_page = reverse_lazy('login') # Redirect to login after logout
