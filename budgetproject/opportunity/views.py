# opportunity/views.py

from django.shortcuts import render

def dashboard_view(request):
    # Change 'dashboard.html' to the full path
    return render(request, 'opportunity/dashboard.html')
