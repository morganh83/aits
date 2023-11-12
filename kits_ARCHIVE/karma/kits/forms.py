from django.contrib.admin.widgets import FilteredSelectMultiple
from django import forms
from django.forms import ModelForm
from .models import Rule, revTicket, punishTicket
from django.forms import modelformset_factory
from django.core.validators import MaxLengthValidator, MinLengthValidator


class ConfigForm(forms.Form):
    config = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'cols': 40, 'rows': 30}), label='')

class TicketsForm(ModelForm):
    class Meta:
        model = punishTicket
        fields = "__all__"
        widgets = {
            # Base Info
            'addtlMods': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Additional Mods'}),
            'ticketLink': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ticket Link'}),
            'counterLink': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Counter Link'}),

            # Warnings
            'punishment': forms.Select(attrs={'class': 'form-control'}),
            'banTime': forms.Select(attrs={'class': 'form-control'}),
            'banTimeOther': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Other Ban Length'}),
            'reason': forms.Textarea(attrs={'class': 'form-control', 'rows': '3', 'placeholder': 'Reason/Notes'}),
            'discName': forms.NumberInput(attrs={'type': 'number', 'class': 'form-control', 'minlength': '17', 'placeholder': 'Offender Disc ID'}),
            'userName': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Player Name'}),
            'steamId': forms.NumberInput(attrs={'type': 'number', 'class': 'form-control', 'minlength': '17', 'placeholder': 'Offender Steam ID'}),
        }


class RTicketsForm(ModelForm):
   class Meta:
       model = revTicket
       fields = "__all__"
       widgets = {
             # Base Info
            'addtlMods': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Additional Mods'}),
            'ticketLink': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ticket Link'}),
            'counterLink': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Counter Link'}),
            
            # Revives
            'userName': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Player Name'}),
            'steamId': forms.NumberInput(attrs={'class': 'form-control', 'type': 'number', 'minlength': '17', 'placeholder': 'Revive Steam ID'}),
            'growth': forms.NumberInput(attrs={'class': 'form-control', 'type': 'number', 'step': '0.01', 'placeholder': 'Growth'}),
            'discName': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Revive Disc Name'}),
            'dinoName': forms.Select(attrs={'class': 'form-control'}),
            'revd': forms.CheckboxInput(attrs={'type': 'checkbox', 'class': 'form-check-input'}),
       }
