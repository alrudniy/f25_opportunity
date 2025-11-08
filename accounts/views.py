from django.contrib.auth import login as auth_login
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.views.generic import FormView
from django.contrib import messages
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


class DeleteAccountView(FormView):
    template_name = 'accounts/delete_account.html'
    form_class = EmailAuthenticationForm
    success_url = reverse_lazy('welcome')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs

    def form_valid(self, form):
        user = form.get_user()
        user.delete()
        messages.success(self.request, "Account deleted successfully.")
        return super().form_valid(form)
