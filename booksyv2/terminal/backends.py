from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model

#This file crates custom login function using email to log in account, it also checks if account exists and if password is correct
class EmailBackend(ModelBackend):
    def authenticate(self, request, email = None, password = None, **kwargs):
        UserModel= get_user_model()
        try:
            user = UserModel.objects.get(email=email)
            if user.check_password(password):
                user.backend = 'terminal.backends.EmailBackend'
                return user
        except UserModel.DoesNotExist:
            return None
        
    def get_user(self, user_id):
        UserModel= get_user_model()
        try:
            return UserModel.objects.get(pk=user_id)
        except UserModel.DoesNotExist:
            return None