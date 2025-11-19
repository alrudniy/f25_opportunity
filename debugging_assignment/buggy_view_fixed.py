from django.shortcuts import render

# A small in-memory dataset (similar to company_home)
ALL_PROJECTS = [
    {'id': 1, 'title': 'AI-Powered Chatbot for Customer Service', 'field': 'Artificial Intelligence',
     'description': 'Developing a chatbot using NLP to enhance support.'},
    {'id': 2, 'title': 'Sustainable Energy Management System', 'field': 'Renewable Energy',
     'description': 'Monitor & optimize energy consumption using IoT.'},
    {'id': 3, 'title': 'Smart City Traffic Management', 'field': 'Urban Planning',
     'description': 'Alleviate traffic congestion using real-time data.'},
    {'id': 4, 'title': 'Blockchain for Supply Chain Traceability', 'field': 'Blockchain',
     'description': 'Track products from origin to consumer via DLT.'},
]

def buggy_search_fixed(request):
    """
    Corrected version of the buggy view for VS Code debugging practice.

    Bugs fixed:
    (1) Handled missing 'q' parameter to prevent AttributeError.
    (2) Used '!=' for string comparison instead of 'is not'.
    (3) Corrected the misspelled dictionary key 'descriptionn' to 'description'.
    """
    # ---- FIX 1: Use a default empty string if 'q' is missing to prevent AttributeError.
    query = (request.GET.get('q') or "").strip()

    field_filter = request.GET.get('field', 'All')
    projects = ALL_PROJECTS.copy()

    # ---- FIX 2: Use '!=' for equality check, as 'is not' checks for object identity.
    if field_filter != 'All':
        projects = [p for p in projects if p['field'] == field_filter]

    # ---- FIX 3: Corrected misspelled key 'descriptionn' to 'description'.
    def predicate(p):
        return query.lower() in p['title'].lower() or query.lower() in p['description'].lower()

    if query:
        projects = list(filter(predicate, projects))

    return render(request, 'pages/buggy_search.html', {
        'projects': projects,
        'current_query': query,
        'current_field': field_filter,
    })
