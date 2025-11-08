from django.urls import path
from django.contrib.auth.views import LogoutView
from .views import RegisterView, CustomLoginView, DeleteAccountView

urlpatterns = [
    path('login/', CustomLoginView.as_view(), name='login'),
    path('register/', RegisterView.as_view(), name='register'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('delete/', DeleteAccountView.as_view(), name='delete_account'),
]
