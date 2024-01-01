from django import forms
from django.contrib.auth.models import User

class CompleteUserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'email']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'input100', 'placeholder': 'Username'}),
            'email': forms.TextInput(attrs={'class': 'input100', 'placeholder': 'Email'}),
            # 'password': forms.PasswordInput(attrs={'class': 'input100', 'placeholder': 'Password'}),
            # 'password': forms.TextInput(attrs={'class': 'input100', 'name': 'pass', 'type': 'password', 'placeholder': 'Password'}),
        }
