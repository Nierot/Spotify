from django import forms

class UsernameForm(forms.Form):
    username = forms.CharField(
        label='Username',
        max_length=50,
        widget=forms.TextInput(attrs={'class': 'form-control'})
        )