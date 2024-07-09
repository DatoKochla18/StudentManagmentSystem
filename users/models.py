from django.db import models
from django.contrib.auth.models import AbstractUser 
# Create your models here.
class CustomUser(AbstractUser):
    is_student=models.BooleanField(default=True)

    def is_student_user(self):
        return self.is_student==1
    def is_teacher_user(self):
        return self.is_student==0
    def is_admin(self):
        return self.is_superuser==1
    
    