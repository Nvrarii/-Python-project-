from django import forms
from .models import Profile

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['avatar']
        widgets = {
            'avatar': forms.ClearableFileInput(attrs={'class': 'form-control-file'}),
        }
        labels = {
            'avatar': 'Avatar',
        }
        help_texts = {
            'avatar': 'Upload a new avatar image.',
        }