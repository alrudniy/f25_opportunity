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
