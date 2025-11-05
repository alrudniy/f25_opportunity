from django.shortcuts import render

def communication_tools_view(request):
    """
    A view that renders the communication tools page with a list of organizations.
    """
    organizations = [
        {'id': 1, 'name': 'Org A', 'contact_email': 'contact@orga.com'},
        {'id': 2, 'name': 'Org B', 'contact_email': 'contact@orgb.com'},
        {'id': 3, 'name': 'Org C', 'contact_email': 'contact@orgc.com'},
    ]
    context = {
        'organizations': organizations,
    }
    return render(request, 'communication_tools.html', context)
