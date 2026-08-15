"""URL configuration for Northstar Chatbot Support App."""
from django.urls import path
from . import views

urlpatterns = [
    path('', views.chatbot, name='chatbot'),
    path('chat/', views.chatbot, name='chatbot_alt'),
    path('chat/api/', views.chat_api, name='chat_api'),
]
