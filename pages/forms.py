from django import forms
from .models import Experience

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
