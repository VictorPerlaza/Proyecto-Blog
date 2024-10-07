from django import forms
from django.contrib.auth.models import User
from .models import Author

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']

class AuthorProfileForm(forms.ModelForm):
    class Meta:
        model = Author
        fields = ['bio']  # Campo para la biografía
