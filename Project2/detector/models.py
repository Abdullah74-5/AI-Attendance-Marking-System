from django.db import models

# Create your models here.
# detector/models.py
from django.db import models
from django.utils import timezone

class Student(models.Model):
    name = models.CharField(max_length=100)
    roll_number = models.CharField(max_length=50, unique=True)
    face_embedding = models.JSONField(blank=True, null=True) # Stores 128D array
    registered_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({self.roll_number})"

class Attendance(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    date = models.DateField(default=timezone.now)
    time = models.TimeField(auto_now_add=True)
    status = models.CharField(max_length=10, default="Present")

    class Meta:
        unique_together = ('student', 'date') # Prevents duplicate entries on the same day

    def __str__(self):
        return f"{self.student.name} - {self.date}"