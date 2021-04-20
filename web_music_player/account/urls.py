from django.urls import path, include
from . import views

app_name = 'site_account'
urlpatterns = [
    # path('signup/', views.OwnSignupView.as_view(), name='signup'),
    path('signup/', views.register, name='signup'),
    path('login/', views.OwnLoginView.as_view(), name='login'),
    path('logout/', views.OwnLogoutView.as_view(), name='logout'),
    path('update/<int:pk>', views.OwnAccountUpdateView.as_view(), name='update'),
    path('password/', views.OwnPasswordChangeView.as_view(), name='password'),
    # path('password_change_done/', views.OwnPasswordChangeDoneView.as_view(), name='password_change_done'),
]
