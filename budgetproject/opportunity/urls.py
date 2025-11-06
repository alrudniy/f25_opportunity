# opportunity/urls.py

from django.urls import path
from . import views

urlpatterns = [
    # Define the dashboard URL here
    path('dashboard/', views.dashboard_view, name='dashboard'),
]