from django import forms
from user.models import Userbase, Profile
from django.contrib.auth.forms import UserCreationForm

# class UserSignupForm(UserCreationForm):
class UserSignupForm(forms.ModelForm):
    accept_t_and_c = forms.BooleanField(label='', required=True)

    class Meta:
        model = Userbase
        fields = [
            'username', 'password', 'first_name', 'last_name',
            'email', 'country', 'gender', 'age',
        ]
        # exclude = ['date_joined']
        widgets = {
            'email': forms.TextInput(attrs={'placeholder': 'E-mail Address'}),
            'username': forms.TextInput(attrs={'placeholder': 'Username'}),
            'password': forms.TextInput(attrs={
                'placeholder': 'Password', 'type': 'password'}),
            'first_name': forms.TextInput(attrs={'placeholder': 'First Name'}),
            'last_name': forms.TextInput(attrs={'placeholder': 'Last Name'}),
        }

class UserUpdateForm(UserSignupForm):
    pass

    class Meta(UserSignupForm.Meta):
        pass
        # widgets = {
        #     'email': forms.TextInput(attrs={'placeholder': 'E-mail Address'}),
        #     'username': forms.TextInput(attrs={'placeholder': 'Username'}),
        #     'password': forms.TextInput(attrs={
        #         'placeholder': 'Password',
        #         'type': 'password',
        #         'readonly': True,}),
        #     'first_name': forms.TextInput(attrs={'placeholder': 'First Name'}),
        #     'last_name': forms.TextInput(attrs={'placeholder': 'Last Name'}),
        # }


class UserLoginForm(forms.ModelForm):
    remember_me = forms.BooleanField(label='Remember Me', required=False)
    
    class Meta:
        model = Userbase
        fields = ['username', 'password']
        widgets = {
            'username': forms.TextInput(attrs={'placeholder': 'Username'}),
            'password': forms.TextInput(attrs={
                'placeholder': 'Password', 'type': 'password'}),
        }
