from django import forms
from .models import Profile

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