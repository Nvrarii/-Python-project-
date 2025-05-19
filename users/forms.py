from django import forms
from .models import Profile
from bookings.models import User
from django.contrib.auth.forms import UserCreationForm

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['email', 'name', 'phone', 'password1', 'password2']

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['name', 'phone', 'avatar', 'bio', 'location']
        widgets = {
            'avatar': forms.ClearableFileInput(attrs={'class': 'form-control-file'}),
            'bio': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'location': forms.TextInput(attrs={'class': 'form-control'}),
        }
        labels = {
            'avatar': 'Avatar',
            'bio': 'About Me',
            'location': 'Location',
            'name': 'Full Name',
            'phone': 'Phone Number',
        }