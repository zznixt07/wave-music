from django import forms
from django.contrib.auth.models import User
from user.models import Profile


class UserRemoveForm(forms.ModelForm):
    email = forms.EmailField()
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']
        

class UserCreateForm(forms.ModelForm):

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

class UserUpdateForm(UserCreateForm):
    pass

    class Meta(UserCreateForm.Meta):
        pass