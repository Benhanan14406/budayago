from django.db import models
from pembelajaran.models import Course
from cloudinary.models import CloudinaryField

# Create your models here.
class Lesson(models.Model):
    title = models.CharField(max_length=100)
    difficulty = models.CharField(max_length=20)
    xp_reward = models.IntegerField()
    course = models.OneToOneField(to=Course, on_delete=models.CASCADE, related_name="quiz", primary_key=True)

class Question(models.Model):
    number = models.IntegerField()
    lesson = models.ForeignKey(to=Lesson, on_delete=models.CASCADE, related_name="soal")
    question_type = models.CharField(max_length=12)
    question = models.TextField()

    class Meta:
        unique_together = ('number', 'lesson')

class SoalSusun(Question):
    answer = models.TextField()

class OpsiGambar(models.Model):
    question = models.ForeignKey(to=Question, on_delete=models.CASCADE)
    gambar = CloudinaryField('image')
    is_correct = models.BooleanField(default=False)

class OpsiSusun(models.Model):
    question = models.ForeignKey(to=SoalSusun, on_delete=models.CASCADE)
    text = models.CharField(max_length=100)

class OpsiMatching(models.Model):
    question = models.ForeignKey(to=Question, on_delete=models.CASCADE)
    text = models.CharField(max_length=100)
    partner = models.ForeignKey(to='self', on_delete=models.CASCADE, null=True)