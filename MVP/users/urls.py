from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = 'users'

urlpatterns = [
    path('login/', views.Login.as_view(), name='login'),
    path('registration/', views.Register.as_view(), name='registration'),
    path('logout/', views.Logout.as_view(), name='logout'),
    path('profile/', views.profile, name='profile'),
    path('reset-password/', views.ResetPasswordViews.as_view(), name='reset_password'),
    path('check_mail/', views.check_mail, name='check_mail'),
    path('password-reset-confirm/<uidb64>/<token>/',
         views.ResetPasswordConfirmView.as_view(template_name='users/reset_password_confirm.html'),
         name='reset_password_confirm'),
    path('password-reset-complete/',
         auth_views.PasswordResetCompleteView.as_view(template_name='users/reset_password_complete.html'),
         name='password_reset_complete'),
]