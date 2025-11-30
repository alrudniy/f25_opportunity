from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import get_user_model

User = get_user_model()

class UserRegistrationForm(UserCreationForm):
    user_type = forms.ChoiceField(choices=User.UserType.choices, widget=forms.RadioSelect)

    class Meta:
        model = User
        # Include email and user_type in registration fields
        fields = ('username', 'email', 'password1', 'password2', 'user_type')
        # If you want email to be the primary identifier and login field,
        # you'll need to adjust AUTH_USER_MODEL in settings.py and potentially this form.
        # For now, we stick to username as primary identifier as per default AbstractUser.

class EmailAuthenticationForm(AuthenticationForm):
    # Field is still named "username" internally by Django's AuthenticationForm;
    # we'll label it clearly as Email for the user.
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].label = 'Email or Username' # Allow login by email or username
        self.fields['username'].widget.attrs.update({'placeholder': 'you@example.com or username', 'autofocus': True})
        self.fields['password'].widget.attrs.update({'placeholder': 'password'})

class UserProfileForm(forms.ModelForm):
    """
    Form for updating user profile fields directly on the User model.
    """
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'university', 'class_year')
        # Note: We are not including username, email, or user_type here for editing
        # as these are typically managed separately or have stricter rules.
        # If you need to edit these, add them to 'fields' and handle accordingly.

        widgets = {
            'first_name': forms.TextInput(attrs={'placeholder': 'Enter your first name'}),
            'last_name': forms.TextInput(attrs={'placeholder': 'Enter your last name'}),
            'university': forms.TextInput(attrs={'placeholder': 'Enter your university name'}),
            'class_year': forms.TextInput(attrs={'placeholder': 'e.g., 2025'}),
        }
        labels = {
            'first_name': 'First Name',
            'last_name': 'Last Name',
            'university': 'University',
            'class_year': 'Class Year',
        }
