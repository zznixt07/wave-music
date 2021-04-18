from django.urls import path, include
from . import views

app_name = 'site_account'
urlpatterns = [
    path('signup/', views.OwnSignupView.as_view(), name='signup'),
    path('login/', views.OwnLoginView.as_view(), name='login'),
    path('logout/', views.OwnLogoutView.as_view(), name='logout'),
    path('update/<int:pk>', views.OwnAccountUpdateView.as_view(), name='update'),
    path('password/', views.OwnPasswordChangeView.as_view(), name='password'),
]
