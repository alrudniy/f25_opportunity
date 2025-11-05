from django.shortcuts import render, redirect
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required

@login_required
def home_view(request):
    """
    Displays the home page.
    """
    return render(request, 'dylan_opportunities/home.html')

def logout_view(request):
    """
    Logs the user out and redirects to the login page.
    """
    logout(request)
    return redirect('dylan_opportunities:login')
