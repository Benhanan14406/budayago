from django.urls import path, include
from . import views

app_name = 'main'

urlpatterns = [
    path('', views.home, name='home'),
    path('token/', views.get_jwt_token, name='get_token'),
    path('projects/', views.projects, name='projects'),
    path('user-profile/', include('user_profile.urls')),
    path('chat/', include('ai_conversation.urls')),
]

