from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = 'dylan_opportunities'
urlpatterns = [
    path('home/', views.home_view, name='home'),
    path('login/', auth_views.LoginView.as_view(template_name='dylan_opportunities/login.html'), name='login'),
    path('logout/', views.logout_view, name='logout'),
]
