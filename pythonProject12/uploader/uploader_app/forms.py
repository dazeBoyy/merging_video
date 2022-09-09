from django import forms
from .models import Blog
from django.forms import ClearableFileInput

class BlogForm(forms.ModelForm):
    class Meta:
        model = Blog
        fields = ['author', 'title', 'file']
        widgets = {
            'file': forms.FileInput(attrs={'multiple': ''}),
        }