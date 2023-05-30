from django.http import HttpResponseRedirect
from django.views.decorators.cache import never_cache
from django.views.generic.base import View
from django.views.generic.edit import FormView
from django.contrib.auth import login, logout
from django.contrib.auth.models import User
from django.contrib.auth.views import PasswordResetView, PasswordResetConfirmView
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import render, redirect

from .forms import RegisterForm, UserForm, ProfileForm
from main.models import Profile

import os
import glob

# Create your views here.

class Register(FormView):
    form_class = RegisterForm
    success_url = '/user/login'
    template_name = 'users/registration.html'

    def form_valid(self, form):
        form.save()
        return super(Register, self).form_valid(form)
    
    def form_invalid(self, form):
        return super(Register, self).form_invalid(form)


class Login(FormView):
    form_class = AuthenticationForm
    success_url = '/'
    template_name = 'users/login.html'

    def form_valid(self, form):
        self.user = form.get_user()

        login(self.request, self.user)
        return super(Login, self).form_valid(form)


class Logout(View):
    def get(self, request):
        logout(request)
        return HttpResponseRedirect('/')


class ResetPasswordViews(SuccessMessageMixin, PasswordResetView):
    template_name = 'users/reset_password.html'
    email_template_name = 'users/reset_password_email.html'
    subject_template_name = 'users/reset_password_subject'
    success_message = "Мы отправили вам по электронной почте инструкцию по установке пароля"
    success_url = '/user/check_mail/'


def check_mail(request):
    return render(request, 'users/check_mail.html')


class ResetPasswordConfirmView(PasswordResetConfirmView):
    success_url = '/user/password-reset-complete/'


@never_cache
def profile(request):
    user_obj = User.objects.filter(id=request.user.id)
    user_icon = Profile.objects.filter(user=request.user).first().icon
    
    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=request.user)
        profile_form = ProfileForm(request.POST, request.FILES, instance=request.user.profile)

        if user_form.is_valid():
            user_form.save()

        if profile_form.is_valid():
            if user_icon != 'img/profile/icon_user_default.png':
                user_icon.delete()  
            
            profile_form.save()

        return redirect('/')
    else:
        user_form = UserForm(instance=request.user)
        profile_form = ProfileForm(instance=request.user.profile)
    print(user_obj)
    context = {
        'user_obj': user_obj[0],
        'user_icon': user_icon,
        'user_form': user_form,
        'profile_form': profile_form,
    }

    return render(request, 'users/profile.html', context)
   