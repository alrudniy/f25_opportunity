from django.urls import path

from .views import opportunity_list_view

urlpatterns = [
    path('list/', opportunity_list_view, name='opportunity-list-page'),
]
