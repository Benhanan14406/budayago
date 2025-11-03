from rest_framework import serializers
from .models import *

class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = '__all__'

class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = '__all__'

class SoalSusunSerializer(serializers.ModelSerializer):
    class Meta:
        model = SoalSusun
        fields = '__all__'

class OpsiGambarSerializer(serializers.ModelSerializer):
    class Meta:
        model = OpsiGambar
        fields = '__all__'

class OpsiMatchingSerializer(serializers.ModelSerializer):
    class Meta:
        model = OpsiMatching
        fields = '__all__'

class OpsiSusunSerializer(serializers.ModelSerializer):
    class Meta:
        model = OpsiSusun
        fields = '__all__'