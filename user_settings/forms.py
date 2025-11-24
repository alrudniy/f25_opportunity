from django import forms
from .models import UserSettings

class UserSettingsForm(forms.ModelForm):
    class Meta:
        model = UserSettings
        fields = ['receive_updates', 'public_experience', 'notifications_on', 'theme']
        widgets = {
            'theme': forms.RadioSelect,
        }
        labels = {
            'receive_updates': 'Receive email updates',
            'public_experience': 'Make my experience profile public',
            'notifications_on': 'Enable notifications',
            'theme': 'Color Theme',
        }
