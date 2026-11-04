from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class CustomUser(AbstractUser):
    class Role(models.TextChoices):
        STUDENT = 'STUDENT', 'Student'
        INSTRUCTOR = 'INSTRUCTOR', 'Instructor'
        ADMIN = 'ADMIN', 'Administrator'

    role = models.CharField(max_length=10, choices=Role.choices, default=Role.STUDENT)
    course = models.CharField(max_length=100, blank=True, null=True)

    @property
    def can_access_admin_panel(self):
        return self.is_active and (self.is_superuser or self.role == self.Role.ADMIN)
