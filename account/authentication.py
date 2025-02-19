# your_app_name/authentication.py

from django.contrib.auth.backends import BaseBackend
from .models import User, TempUser



class CustomUserBackend(BaseBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            user = User.objects.get(email=username)
            if user.check_password(password):
                return user
        except User.DoesNotExist:
            return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None 


class TempUserBackend(BaseBackend):
    def authenticate(self, request, username=None, otp=None, **kwargs):
        try:
            user = TempUser.objects.get(phone=username)
            if user.verify_otp(otp):
            # if user:
                return user
             
        except TempUser.DoesNotExist:
            return None

    def get_user(self, user_id):
        try:
            return TempUser.objects.get(pk=user_id)
        except TempUser.DoesNotExist:
            return None
