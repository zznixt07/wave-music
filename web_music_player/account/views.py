import logging
from django.views import generic
from django.shortcuts import render, redirect
from django.urls import reverse, reverse_lazy
from django.contrib.auth import views as auth_views
from .forms import UserSignupForm, UserLoginForm

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
