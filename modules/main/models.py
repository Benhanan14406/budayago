from django.db import models
from django.contrib.auth.models import User
import uuid
from cloudinary.models import *
from datetime import date, timedelta

# Create your models here.

'''
==================
README PLEASE UwU
==================

Konsep relationnya itu mostly spti duolingo, bedanya
- Course merupakan bahasa yang ingin dipelajari
- Gaada section sama unit, Jadi course nyambung ke lesson
- Lesson itu kayak section di duolingo, dan sifatnya level gitu 
- Course ke Lesson OneToMany Relation
- User ke Course itu ManyToMany Relation
- UserProfile itu inherit User Django dengan attr tambahan

Kalau ada yang bingung lagi contact me ajah, sisanya sama spti di dbdiagram :D
https://dbdiagram.io/d/Budayago-690790246735e11170db9661
'''
class RegionalLanguages(models.TextChoices):
    SUNDA = "SU", "Sunda",
    JAWA = "JW", "Jawa",
    MINANG = "MN", "Minang",
    BATAK = "BAT", "Batak",
    MADURA = "MD", "Madura",
    MELAYU = "ML", "Melayu",
    BALI = "BI", "Bali"

class QuestionType(models.TextChoices):
    PILIHAN_GANDA = "PG", "Pilihan Ganda"
    ISIAN_SINGKAT = "IS", "Isian Singkat"
    BENAR_SALAH = "BS", "Benar / Salah"

class LessonType(models.TextChoices):
    QUESTION = "QS", "Question Lesson"
    AI_CONVERSATION = "AI", "AI Conversation Lesson"


class Language(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True)
    code = models.CharField(max_length=10, unique=True, choices=RegionalLanguages.choices)
    name = models.CharField(max_length=50)

    class Meta:
        app_label = 'main'

    def __str__(self):
        return self.name

class Course(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True)
    base_language = models.ForeignKey(Language, on_delete=models.CASCADE, related_name='base_courses')
    target_language = models.ForeignKey(Language, on_delete=models.CASCADE, related_name='target_courses')
    title = models.CharField(max_length=100, blank=False, null=False)
    description = models.TextField()

    def __str__(self):
        return f"{self.title} ({self.base_language} → {self.target_language})"


class Lesson(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='lessons')
    title = models.CharField(max_length=100)
    order = models.PositiveIntegerField(help_text="Urutan lesson dalam course")
    type = models.CharField(max_length=50, choices=LessonType.choices)
    xp_reward = models.PositiveIntegerField(default=10, null=False, blank=False)
    difficulty = models.CharField(max_length=20, choices=[
        ("EASY", "Easy"),
        ("MEDIUM", "Medium"),
        ("HARD", "Hard"),
    ], default="EASY")

    def __str__(self):
        return f"{self.course.title} - {self.title}"
    
class Question(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True)
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, related_name='questions')
    question_type =  models.CharField(max_length=10, choices=QuestionType.choices)
    question = models.TextField(blank=False, null=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    order = models.PositiveBigIntegerField(default=0, help_text="Nomor soal dalam question")


class Option(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='options')

    text = models.CharField(max_length=100, blank=False, null=False, help_text="Pilihan jawaban")
    is_correct = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Explanation(models.Model):
    question = models.OneToOneField(Question, on_delete=models.CASCADE, related_name='explanation')
    answer = models.TextField()
    audio_answer = CloudinaryField('audio', resource_type='video', blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    email = models.EmailField(unique=True, primary_key=True)
    name = models.CharField(max_length=70, blank=False, null=False)
    age = models.IntegerField(default=0, blank=True, null=True)
    avatar = CloudinaryField('image', null=True)
    region = models.CharField(max_length=50, blank=False, null=True)
   
    courses = models.ManyToManyField(Course, through="CourseProgress", related_name='enrolled_users')
    current_course = models.ForeignKey(Course, on_delete=models.SET_NULL, null=True, blank=True, related_name='active_users')

    xp = models.PositiveBigIntegerField(default=0, blank=True)
    level = models.PositiveIntegerField(default=1, blank=True)
    gems = models.PositiveBigIntegerField(default=0, blank=True)

    streak = models.PositiveIntegerField(default=0, blank=True)
    last_streak_date = models.DateField(null=True, blank=True)

    last_login = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.username

class CourseProgress(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)

    started_at = models.DateTimeField(auto_now_add=True)
    last_view = models.DateTimeField(auto_now=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.name} - {self.course.title}"
    
class LessonProgress(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)

    completed = models.BooleanField(default=False)
    progress_percentage = models.FloatField(default=0.0, help_text="Persentase penyelesaian lesson (0–100%)")
    last_attempt = models.DateTimeField(auto_now=True)
    
class AIConversation(models.Model):
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, related_name='ai_conversations')
    topic = models.CharField(max_length=100)
    prompt = models.TextField(help_text="Instruksi atau konteks percakapan AI")
    max_turns = models.PositiveIntegerField(default=5)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class DailyStreak(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='daily_streak')
    date = models.DateField(help_text="Date of the streak")
    total_minutes = models.PositiveIntegerField(default=0, help_text="Total menit menggunakan app dalam satu hari")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('user', 'date')

