from django.db import models
from datetime import datetime
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
# Create your models here.


class UserManager(BaseUserManager):
    def creating_user(self,email,date_of_birth,password=None):
        if not email:
            raise ValueError("You need an email to proceed!")

        user=self.model(
            email=self.normalize_email(email),
            date_of_birth=date_of_birth
        )
        user.set_password(password)
        user.save()
        return user


class MyUser(AbstractBaseUser):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    email = models.EmailField(verbose_name="email address",unique=True,)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    is_active = models.BooleanField(default=True)

    # Required fields for custom user models
    USERNAME_FIELD = 'email'
    
    objects=UserManager()

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

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