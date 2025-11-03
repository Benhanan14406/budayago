from django.shortcuts import render
from rest_framework import viewsets
from .models import *
from serializers import *

# Create your views here.
class LessonViewSet(viewsets.ModelViewSet):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer

class QuestionViewSet(viewsets.ModelViewSet):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer

class SoalSusunViewSet(viewsets.ModelViewSet):
    queryset = SoalSusun.objects.all()
    serializer_class = SoalSusunSerializer