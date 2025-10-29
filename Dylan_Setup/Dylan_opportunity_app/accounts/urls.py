
from django.urls import path
from .views import signup_view, login_view, CustomPasswordResetView

urlpatterns = [
    path('signup/', signup_view, name='signup'),
    path('login/', login_view, name='login'),
    path('password_reset/', CustomPasswordResetView.as_view(), name='password_reset'),
]
