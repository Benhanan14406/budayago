from django.db import models

# Create your models here.
class Course(models.Model):
    id = models.UUIDField(primary_key=True)
    title = models.CharField(max_length=255)
    author = models.CharField(null=True)
    content = models.TextField()