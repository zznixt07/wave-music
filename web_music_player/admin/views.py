from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

# from blog.models import Post
from .forms import UserRemoveForm, UserUpdateForm, UserCreateForm
from user.auth import admin_only
from user.models import Userbase

@login_required
@admin_only
def admin_profile(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, request.FILES, instance=request.user)
        if u_form.is_valid():
            u_form.save()
            messages.success(request, f'Your account has been updated')
            context = {
                'activate_profile': 'active',
            }
            return redirect('/admin-dashboard/profile')
    else:
        u_form = UserUpdateForm(instance=request.user)

    context =  {
        'u_form': u_form,
    }
    return render(request, 'admins/admin-profile.html', context)


@login_required
@admin_only
def admin_dashboard(request):
    users = Userbase.objects.filter(is_superuser=0)
    users_count = users.count()
    admins = Userbase.objects.filter(is_superuser=1)
    admins_count = admins.count()
    # posts_count = Post.objects.all().count()
    total_users = Userbase.objects.all().count()
    context = {
        'users': users_count,
        'admins': admins_count,
        'posts': posts_count,
        'total_users': total_users,
    }
    return render(request, 'admins/adminDashboard.html', context)

@login_required
@admin_only
def get_user(request):
    users_all = Userbase.objects.all()
    users = users_all.filter(is_superuser=0)
    context = {
        'users': users,
    }
    return render(request, 'admins/displayUser.html', context)

@login_required
@admin_only
def get_admin(request):
    users_all = Userbase.objects.all()
    admins = users_all.filter(is_superuser=1)
    context = {
        'admins': admins,
    }
    return render(request, 'admins/displayAdmin.html', context)

@login_required
@admin_only
def update_user_to_admin(request, user_id):
    user = Userbase.objects.get(id=user_id)
    user.is_superuser = 1
    user.save()
    messages.add_message(request, messages.SUCCESS, f'{user.username} has been updated to Admin')
    return redirect('/admin-dashboard')

@login_required
@admin_only
def update_admin_to_user(request, user_id):
    user = Userbase.objects.get(id=user_id)
    user.is_superuser = 0
    user.save()
    messages.add_message(request, messages.SUCCESS, f'{user.username} has been updated to User')
    return redirect('/admin-dashboard')

@login_required
@admin_only
def register_user_admin(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'User account has been created successfully')
            return redirect('/admin-dashboard')
    else:
        form = UserRegisterForm()
    return render(request, 'admins/add-user-admin.html', {'form': form})


@login_required
@admin_only
def del_user(request, username):    
    u = Userbase.objects.get(username = username)
    u.delete()
    messages.add_message(request, messages.SUCCESS, f'{username} has been deleted successfully.')            
    return redirect('/admin-dashboard')



