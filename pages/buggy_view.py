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

def fixed_search(request):
    """
    Corrected version of buggy_search.
    Fixes:
    (1) Avoid AttributeError when 'q' is missing.
    (2) Use '!=' instead of 'is not' for string comparison.
    (3) Fix misspelled key 'descriptionn'.
    """
    # ---- FIX 1: safely handle missing query string
    query = request.GET.get('q', '')  # default empty string
    query = query.strip()

    field_filter = request.GET.get('field', 'All')
    projects = ALL_PROJECTS.copy()

    # ---- FIX 2: use != instead of `is not`
    if field_filter != 'All':
        projects = [p for p in projects if p['field'] == field_filter]

    # ---- FIX 3: correct key name and avoid repeated .lower() calls
    if query:
        q = query.lower()

        def predicate(p):
            return (
                q in p['title'].lower()
                or q in p['description'].lower()   # FIXED KEY
            )

        projects = list(filter(predicate, projects))

    return render(request, 'pages/buggy_search.html', {
        'projects': projects,
        'current_query': query,
        'current_field': field_filter,
    })
