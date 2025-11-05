from django.urls import path
from . import views

app_name = 'messenger'

urlpatterns = [
    path('send/', views.SendMessageView.as_view(), name='send_message'),
    path('broadcast/', views.BroadcastMessageView.as_view(), name='broadcast_message'),
]
