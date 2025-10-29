
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
