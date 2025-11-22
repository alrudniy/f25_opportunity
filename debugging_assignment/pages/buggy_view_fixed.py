from django.shortcuts import render


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

def buggy_search(request):
    query = (request.GET.get('q') or "").strip() 


    field_filter = request.GET.get('field', 'All')
    projects = ALL_PROJECTS.copy()

    if field_filter != 'All':

        projects = [p for p in projects if p['field'] == field_filter]

    def predicate(p):
        
        q = query.lower()
        return q in p['title'].lower() or q in p['description'].lower()

    if query:
        projects = list(filter(predicate, projects))

    return render(request, 'pages/buggy_search.html', {
        'projects': projects,
        'current_query': query,
        'current_field': field_filter,
    })
