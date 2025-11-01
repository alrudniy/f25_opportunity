from django import forms
from .models import Experience, StudentProfile


class StudentProfileForm(forms.ModelForm):
    first_name = forms.CharField(label="First Name", max_length=150, required=True)
    last_name = forms.CharField(label="Last Name", max_length=150, required=True)

    class Meta:
        model = StudentProfile
        fields = ['profile_picture', 'university', 'class_year', 'about_me']
        widgets = {
            'about_me': forms.Textarea(attrs={'rows': 4}),
        }

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if self.user:
            self.fields['first_name'].initial = self.user.first_name
            self.fields['last_name'].initial = self.user.last_name

    def save(self, commit=True):
        profile = super().save(commit=False)
        
        self.user.first_name = self.cleaned_data['first_name']
        self.user.last_name = self.cleaned_data['last_name']
        
        if commit:
            self.user.save()
            profile.save()
            
        return profile


class ExperienceForm(forms.ModelForm):
    description = forms.CharField(
        min_length=20,
        widget=forms.Textarea(attrs={'rows': 4}),
        help_text="Please enter a description of at least 20 characters."
    )

    class Meta:
        model = Experience
        fields = ['organization_name', 'role', 'experience_type', 'start_date', 'end_date', 'description']
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'end_date': forms.DateInput(attrs={'type': 'date'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        start_date = cleaned_data.get("start_date")
        end_date = cleaned_data.get("end_date")

        if end_date and start_date and end_date < start_date:
            self.add_error('end_date', "End date cannot be before start date.")

        return cleaned_data
