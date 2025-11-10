from django.shortcuts import render
from rest_framework import viewsets
from .models import *
from modules.main.serializers import *
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from rest_framework_simplejwt.tokens import RefreshToken
from django.http import JsonResponse

# Create your views here.
class LessonViewSet(viewsets.ModelViewSet):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer

class QuestionViewSet(viewsets.ModelViewSet):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer

class OptionViewSet(viewsets.ModelViewSet):
    queryset = Option.objects.all()
    serializer_class = OptionSerializer

def home(request):
    return render(request, 'home.html')

@login_required
def get_jwt_token(request):
    """
    Generate JWT token for authenticated user
    """
    user = request.user
    refresh = RefreshToken.for_user(user)
    
    return JsonResponse({
        'refresh': str(refresh),
        'access': str(refresh.access_token),
        'user': {
            'id': user.id,
            'email': user.email,
            'first_name': user.first_name,
            'last_name': user.last_name,
        }
    })

@login_required
def projects(request):
    return JsonResponse({'message': 'Projects endpoint'})
