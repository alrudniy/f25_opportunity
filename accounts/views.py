from django.contrib.auth import login as auth_login
from django.contrib.auth import login as auth_login
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.views.generic import FormView
from .forms import UserRegistrationForm, EmailAuthenticationForm
from django.shortcuts import render # Added for rendering the template
from django.contrib.auth.decorators import login_required # Added for decorator

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

@login_required
def company_about(request):
    context = {
        'display_name': request.user.display_name,
        'mission': "Our mission is to connect passionate volunteers with meaningful opportunities to make a positive impact in their communities.",
        'problems_solved': "We help address community needs by streamlining volunteer recruitment, event management, and opportunity matching, ensuring efficient resource allocation and greater societal benefit.",
        'contact_email': request.user.email,
    }
    return render(request, 'pages/company_about.html', context)
