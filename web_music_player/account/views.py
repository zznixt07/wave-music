import logging
from django.views import generic
from django.shortcuts import render, redirect
from django.urls import reverse, reverse_lazy
from django.contrib.auth import views as auth_views
from .forms import UserSignupForm, UserLoginForm, UserUpdateForm
from django.contrib import messages
from user.models import Profile, Userbase
from django.views.generic.edit import CreateView
from django.contrib.auth.hashers import check_password, make_password

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)
from django.http import HttpResponse

# class OwnSignupView(generic.CreateView):
# class OwnSignupView(CreateView):
#     model = Profile
#     template_name = 'account/signup.html'
#     form_class = UserSignupForm
#     success_url = reverse_lazy('account:login')

def register(request):
    if request.method == 'POST':
        form = UserSignupForm(request.POST)
        if form.is_valid():
            del form.cleaned_data['accept_t_and_c']
            form.cleaned_data['password'] = make_password(form.cleaned_data['password'])
            Userbase(**form.cleaned_data).save()
            messages.success(request, f'Your account has been created!', fail_silently=True)
            return redirect('account:login')
        else:
            messages.error(request, f'Try Again', fail_silently=True)
            
    else:
        form = UserSignupForm()
    return render(request, 'account/signup.html', {'form': form})

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

class OwnPasswordChangeView(auth_views.PasswordChangeView):
    template_name = 'account/password.html'
    
    # form_class = UserUpdateForm
    # success_url = reverse_lazy('account:login')

class OwnPasswordChangeDoneView(auth_views.PasswordChangeDoneView):
    template_name = 'account/passwordChanged.html'
    extra_content = {}
