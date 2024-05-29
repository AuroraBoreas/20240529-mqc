from .models import AppUser

from django.contrib.auth.forms import UserCreationForm
from core.user.models import AppUser

class AppUserRegisterForm(UserCreationForm):
    class Meta:
        model = AppUser
        fields = ('username', 'email', 'password1', 'password2')