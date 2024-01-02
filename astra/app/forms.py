from django import forms
from django.contrib.auth.models import User
from .models import UserProfile
from django.contrib.auth.forms import UserCreationForm

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
        fields = ['discord_id', 'discord_username', 'steam_id', 'timezone', 'languages', 'bio', 'photo', 'alts']

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(UserUpdateForm, self).__init__(*args, **kwargs)
        if user:
            self.fields['email'].initial = user.email
            
class UserCreateForm(UserCreationForm):
    # Additional fields from UserProfile
    discord_id = forms.CharField(max_length=100, required=False)
    discord_username = forms.CharField(max_length=100, required=False)
    steam_id = forms.CharField(max_length=100, required=False)
    timezone = forms.CharField(max_length=5, required=False)
    languages = forms.CharField(max_length=200, required=False)
    bio = forms.CharField(widget=forms.Textarea, required=False)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'discord_id', 'discord_username', 'steam_id', 'timezone', 'languages', 'bio']

    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()
            user_profile = UserProfile.objects.create(
                user=user,
                discord_id=self.cleaned_data['discord_id'],
                discord_username=self.cleaned_data['discord_username'],
                steam_id=self.cleaned_data['steam_id'],
                timezone=self.cleaned_data['timezone'],
                languages=self.cleaned_data['languages'],
                bio=self.cleaned_data['bio']
            )
        return user