from django import forms
from django.contrib.auth.models import User
from .models import UserProfile

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

class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()  # Assuming you want to edit the User's email

    class Meta:
        model = UserProfile
        fields = ['discord_id', 'discord_username', 'steam_id', 'timezone', 'languages', 'bio', 'photo']

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(UserUpdateForm, self).__init__(*args, **kwargs)
        if user:
            self.fields['email'].initial = user.email