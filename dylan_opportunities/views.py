from django.shortcuts import redirect
from django.contrib.auth import logout

def logout_view(request):
    """
    Logs the user out and redirects to the login page.
    """
    logout(request)
    return redirect('dylan_opportunities:login')
