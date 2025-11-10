from django.urls import path
from .views import GeminiChatView

urlpatterns = [
    path('', GeminiChatView.as_view(), name='gemini-chat'),
]