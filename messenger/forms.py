from django import forms
from .models import Volunteer, Organization

class SendMessageToVolunteerForm(forms.Form):
    volunteer = forms.ModelChoiceField(queryset=Volunteer.objects.all(), empty_label="Select a Volunteer")
    subject = forms.CharField(max_length=200, initial="Message from Organization")
    message = forms.CharField(widget=forms.Textarea)

class SendMessageToOrganizationForm(forms.Form):
    organization = forms.ModelChoiceField(queryset=Organization.objects.all(), empty_label="Select an Organization")
    subject = forms.CharField(max_length=200, initial="Message from Volunteer")
    message = forms.CharField(widget=forms.Textarea)

class BroadcastMessageForm(forms.Form):
    subject = forms.CharField(max_length=200, initial="Important Announcement")
    message = forms.CharField(widget=forms.Textarea)
    target_audience = forms.ChoiceField(
        choices=[('volunteers', 'All Volunteers'), ('organizations', 'All Organizations')],
        widget=forms.RadioSelect
    )
