from django.urls import path
from . import views

urlpatterns = [
    path('home', views.send_whatsapp_message, name='send_whatsapp_message'),
    path('webhook/', views.webhook, name='whatsapp_webhook'),
    
]