from django.db import models
from datetime import datetime
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
# Create your models here.

#Created class to create users in forms
class UserManager(BaseUserManager):
    def creating_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("You need an email to proceed!")

        user = self.model(
            email=self.normalize_email(email),
            **extra_fields
        )
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        return self.creating_user(email, password, **extra_fields)

#Model of user that gets info uploaded through function creating_user()
class MyUser(AbstractBaseUser):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    email = models.EmailField(verbose_name="email address",unique=True,)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    # Required fields for custom user models
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name',]
    objects=UserManager()

    # Added option to change permissions
    def has_perm(self, perm, obj=None):
        return self.is_superuser

    def has_module_perms(self, app_label):
        return self.is_superuser
    
    def __str__(self):
        return self.email


TIME_CHOICES = (
    ("10:00", "10:00"),
    ("11:00", "11:00"),
    ("12:00", "12:00"),
    ("13:00", "13:00"),
    ("14:00", "14:00"),
    ("15:00", "15:00"),
    ("16:00", "16:00"),
    ("17:00", "17:00"),
    ("18:00", "18:00"),
    ("19:00", "19:00"),
)

class Appointment(models.Model):
    user= models.ForeignKey(MyUser, on_delete=models.SET_NULL, null=True, blank=True)
    service = models.ForeignKey('Service', on_delete=models.SET_NULL, null=True, blank=True)
    day = models.DateField(default=datetime.now)
    time = models.CharField(max_length=10, choices=TIME_CHOICES, default="10:00")
    time_ordered = models.DateTimeField(default=datetime.now,blank=True)
    def __str__(self):
        return f"{self.user.first_name} | day:{self.day} | time:{self.time}"
    
class Service(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField(blank=True, null=True)
    workers = models.ManyToManyField(MyUser, related_name='services', blank=True)
    duration = models.IntegerField(default=60, help_text="Duration in minutes")

    def __str__(self):
        return self.name