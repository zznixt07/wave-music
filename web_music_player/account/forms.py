from django import forms
from user.models import Userbase, Profile

class UserSignupForm(forms.ModelForm):
    accept_t_and_c = forms.BooleanField(label='',required=True)
    class Meta:
        model = Profile
        fields = [
            'username', 'password', 'first_name', 'last_name',
            'email', 'country', 'gender', 'age',
        ]
        widgets = {
            'email': forms.TextInput(attrs={'placeholder': 'E-mail Address'}),
            'username': forms.TextInput(attrs={'placeholder': 'Username'}),
            'password': forms.TextInput(attrs={
                'placeholder': 'Password', 'type': 'password'}),
            'first_name': forms.TextInput(attrs={'placeholder': 'First Name'}),
            'last_name': forms.TextInput(attrs={'placeholder': 'Last Name'}),
        }

class UserLoginForm(forms.ModelForm):
    remember_me = forms.BooleanField(label='Remember Me',required=True)
    
    class Meta:
        model = Profile
        fields = ['username', 'password']
        widgets = {
            'username': forms.TextInput(attrs={'placeholder': 'Username'}),
            'password': forms.TextInput(attrs={
                'placeholder': 'Password', 'type': 'password'}),
        }


