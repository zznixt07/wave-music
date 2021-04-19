import logging
from django.views import generic
from django.shortcuts import render, redirect
from django.urls import reverse, reverse_lazy
from django.contrib.auth import views as auth_views
from .forms import UserSignupForm, UserLoginForm, UserUpdateForm
from user.models import Profile

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)


# class OwnLoginView(generic.FormView):
#     template_name = 'account/login.html'
#     form_class = UserLoginForm
#     success_url = reverse_lazy('user:index')


class OwnSignupView(generic.CreateView):
    template_name = 'account/signup.html'
    form_class = UserSignupForm
    success_url = reverse_lazy('account:login')


class OwnLoginView(auth_views.LoginView):
    template_name = 'account/login.html'
    # authentication_form = UserLoginForm
    redirect_authenticated_user = True
    success_url = reverse_lazy('user:index')

class OwnLogoutView(auth_views.LogoutView):
    template_name = 'account/login.html'
    next_page = reverse_lazy('account:login')
    success_url = reverse_lazy('account:login')

class OwnAccountUpdateView(generic.UpdateView):
    template_name = 'account/account.html'
    model = Profile
    fields = [
        'username', 'password', 'first_name', 'last_name',
        'email', 'country', 'gender', 'age',
    ]
    # form_class = UserUpdateForm
    success_url = reverse_lazy('user:index')

class OwnAccountUpdateView(generic.UpdateView):
    template_name = 'account/account.html'
    model = Profile
    fields = [
        'username', 'password', 'first_name', 'last_name',
        'email', 'country', 'gender', 'age',
    ]
    # form_class = UserUpdateForm
    success_url = reverse_lazy('user:index')

class OwnPasswordChangeView(auth_views.PasswordChangeView):
    template_name = 'account/password.html'
    
    # form_class = UserUpdateForm
    # success_url = reverse_lazy('account:login')

class OwnPasswordChangeDoneView(auth_views.PasswordChangeDoneView):
    template_name = 'account/passwordChanged.html'
    extra_content = {}
