from django.urls import path
from . import views

app_name = 'main'

urlpatterns = [
    path('', views.home, name='home'),
    path('token/', views.get_jwt_token, name='get_token'),
    path('projects/', views.projects, name='projects'),
]