from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import MyUser

#This is Regisration form
class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    

    class Meta:
        model = MyUser
        fields=('first_name', 'last_name', 'email', 'phone_number','password1', 'password2')

    def safe(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.phone_number = self.cleaned_data['phone_number']

        if commit:
            user.save()
        return user