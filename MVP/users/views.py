from django.http import HttpResponseRedirect
from django.views.decorators.cache import never_cache
from django.views.generic.base import View
from django.views.generic.edit import FormView
from django.views.i18n import set_language
from django.contrib.auth import login, logout
from django.contrib.auth.models import User
from django.contrib.auth.views import PasswordResetView, PasswordResetConfirmView
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.hashers import check_password, make_password
from django.contrib.messages.views import SuccessMessageMixin
from django.utils.translation import gettext as _
from django.shortcuts import render

from .forms import RegisterForm, ProfileForm
from main.models import Profile

import re


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
    success_message = _("Мы отправили вам по электронной почте инструкцию по установке пароля")
    success_url = '/user/check_mail/'


def check_mail(request):
    return render(request, 'users/check_mail.html')


class ResetPasswordConfirmView(PasswordResetConfirmView):
    success_url = '/user/password-reset-complete/'


@never_cache
def profile(request):
    ''' Show and edit the user's profile information. '''

    user_obj = User.objects.get(id=request.user.id)
    user_icon = Profile.objects.filter(user=request.user).first().icon
    error_email = False
    
    if request.method == 'POST':
        profile_form = ProfileForm(request.POST, request.FILES, instance=request.user.profile)

        for field in profile_form:
            if request.POST.get(field.html_name):
                if user_icon != 'img/profile/icon_user_default.png':
                    user_icon.delete()  
            
            profile_form.save()
            user_icon = Profile.objects.filter(user=request.user).first().icon

        if request.POST.get('new_username'):
            new_username = request.POST.get('new_username')
            user_obj.username = new_username
            user_obj.save()

        if request.POST.get('new_email'):
            if re.findall(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b', request.POST.get('new_email')):
                user_obj.email = request.POST.get('new_email')
                user_obj.save()
            else:
                error_email = True

        if request.POST.get('language'):
            request.session['language'] = request.POST['language']

            return set_language(request)

    else:
        profile_form = ProfileForm(instance=request.user.profile)
    
    context = {
        'user_obj': user_obj,
        'user_icon': user_icon,
        'profile_form': profile_form,
        'error_email': error_email
    }

    return render(request, 'users/profile.html', context)


def change_password(request, user_id):
    user_password = User.objects.get(id=user_id)
    old_password = request.POST.get('old_password')
    new_password = request.POST.get('new_password')
    confirm_new_password = request.POST.get('confirm_new_password')
    error_password = []
    
    if request.method == 'POST':
        if not check_password(old_password, user_password.password):
            error_password.append('Старый пароль введен неправильно')

        if new_password != confirm_new_password:
            error_password.append('Пароли не совпадают')
        
        if check_password(new_password, user_password.password):
            error_password.append('Новый пароль совпадает со старым')

        if len(new_password) < 8:
            error_password.append('Пароль должен содержать минимум 8 символов')

        if not bool(re.search(r'\d', new_password)):
            error_password.append('Пароль должен содержать хотя бы одну цифру')

        if not bool(re.search(r'[a-zA-Z]', new_password)):
            error_password.append('Пароль должен содержать хотя бы одну букву')

        if not error_password:
            new_make_password = make_password(new_password, hasher='pbkdf2_sha256')
            user_password.password = new_make_password
            user_password.save()

        return render(request, 'users/reset_password_complete.html')
    
    context = {
        'error_password': error_password
    }

    return render(request, 'users/change_password.html', context)