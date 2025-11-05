from django.shortcuts import render, redirect
from django.views.generic import View
from django.contrib import messages
from .managers import CommunicationManager
from .forms import SendMessageToVolunteerForm, SendMessageToOrganizationForm, BroadcastMessageForm
from .models import Volunteer, Organization

comm_manager = CommunicationManager()

class SendMessageView(View):
    template_name = 'messenger/send_message.html'

    def get(self, request, *args, **kwargs):
        volunteer_form = SendMessageToVolunteerForm()
        organization_form = SendMessageToOrganizationForm()
        return render(request, self.template_name, {
            'volunteer_form': volunteer_form,
            'organization_form': organization_form
        })

    def post(self, request, *args, **kwargs):
        if 'send_to_volunteer' in request.POST:
            form = SendMessageToVolunteerForm(request.POST)
            if form.is_valid():
                volunteer = form.cleaned_data['volunteer']
                subject = form.cleaned_data['subject']
                message_content = form.cleaned_data['message']
                result = comm_manager.send_message_to_volunteer(str(volunteer.id), message_content, subject)
                messages.success(request, result)
                return redirect('messenger:send_message')
            else:
                messages.error(request, "Error sending message to volunteer.")
        elif 'send_to_organization' in request.POST:
            form = SendMessageToOrganizationForm(request.POST)
            if form.is_valid():
                organization = form.cleaned_data['organization']
                subject = form.cleaned_data['subject']
                message_content = form.cleaned_data['message']
                result = comm_manager.send_message_to_organization(str(organization.id), message_content, subject)
                messages.success(request, result)
                return redirect('messenger:send_message')
            else:
                messages.error(request, "Error sending message to organization.")
        
        # If no specific form was handled or there was an error, re-render with forms
        volunteer_form = SendMessageToVolunteerForm(request.POST if 'send_to_volunteer' in request.POST else None)
        organization_form = SendMessageToOrganizationForm(request.POST if 'send_to_organization' in request.POST else None)
        return render(request, self.template_name, {
            'volunteer_form': volunteer_form,
            'organization_form': organization_form
        })

class BroadcastMessageView(View):
    template_name = 'messenger/broadcast_message.html'

    def get(self, request, *args, **kwargs):
        form = BroadcastMessageForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = BroadcastMessageForm(request.POST)
        if form.is_valid():
            subject = form.cleaned_data['subject']
            message_content = form.cleaned_data['message']
            target_audience = form.cleaned_data['target_audience']

            if target_audience == 'volunteers':
                result = comm_manager.broadcast_message_to_volunteers(message_content, subject)
            else: # organizations
                result = comm_manager.broadcast_message_to_organizations(message_content, subject)
            
            messages.success(request, result)
            return redirect('messenger:broadcast_message')
        else:
            messages.error(request, "Error broadcasting message.")
            return render(request, self.template_name, {'form': form})
