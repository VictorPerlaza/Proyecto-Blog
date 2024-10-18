from django import forms
from django.contrib.auth.models import User
from .models import Author , Post , Tag

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email']  # Solo username y email

class AuthorProfileForm(forms.ModelForm):
    class Meta:
        model = Author
        fields = ['bio', 'avatar']  # Incluye el campo de avatar

class PostForm(forms.ModelForm):
    tags = forms.ModelMultipleChoiceField(
        queryset=Tag.objects.all(),
        widget=forms.SelectMultiple(attrs={
            'class': 'select2',
            'multiple': 'multiple',
            'data-placeholder': 'Selecciona etiquetas...',
        }),
        required=False
    )

    class Meta:
        model = Post
        fields = ['title', 'content', 'image', 'category', 'tags']