from django.db import models
from django.contrib.auth import get_user_model

# Create your models here.
class Course(models.Model):
    name=models.CharField(max_length=255)
    description=models.TextField()
    category=models.CharField(max_length=255)
    teacher = models.ForeignKey(
    get_user_model(),
    on_delete=models.CASCADE,
    )
    

class Enrollment(models.Model):
    student = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='enrollments')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='enrollments')
    completed = models.BooleanField(default=False)


class Forum(models.Model):
    customer = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='forum')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='forum')
    message=models.TextField()
    created=models.DateTimeField(auto_now_add=True)
    