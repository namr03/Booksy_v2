from django.db import models

# Create your models here.
class Client(models.Model):
    first_name=models.CharField(max_length=30)
    last_name=models.CharField(max_length=30)
    e_mail=models.EmailField(unique=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)

class Employee(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    is_active = models.BooleanField(default=True)

    # Required fields for custom user models
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

class Tasks(models.Model):
    title = models.CharField(max_length=100)
    description = models.CharField(blank=True)
    timestamp = models.DurationField()
    assigned_to = models.ForeignKey(Employee,on_delete=models.CASCADE, related_name='tasks')