from django.db import models
from datetime import datetime
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
# Create your models here.

#Created class to create users later in forms
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

    def has_perm(self, perm, obj=None):
        return self.is_superuser

    def has_module_perms(self, app_label):
        return self.is_superuser
    
    def __str__(self):
        return self.email

class Service(models.Model):
    title = models.CharField(max_length=100)
    description = models.CharField(blank=True)
    timestart = models.DateTimeField(default=datetime.now, blank=True)
    timestop = models.DateTimeField(default=datetime.now, blank=True)
    assigned_to = models.ForeignKey(MyUser,on_delete=models.CASCADE, related_name='tasks')
    def __str__(self):
        formatted_date_start = self.timestart.strftime("%Y-%m-%d %H:%M")
        formatted_date_end = self.timestop.strftime("%H:%M")
        return f"{self.title} {formatted_date_start} to {formatted_date_end}"