from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.utils.translation import gettext_lazy as _
from django.forms.widgets import ClearableFileInput

from main.models import Profile


class RegisterForm(UserCreationForm):
    username = forms.CharField(label=_('Логин'))
    email = forms.EmailField(label=_('Почта'), required=True)
    password1 = forms.CharField(
        widget=forms.PasswordInput,
        label=_('Пароль')
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput,
        label=_('Повторить пароль')
    )
    
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

    def save(self, commit=True):
        user = super(RegisterForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        
        if commit:
            user.save()
            
        return user
    

class FileInputWidget(ClearableFileInput):
    template_name = 'custom_widgets/input_widget.html'


class ProfileForm(forms.ModelForm):
    icon = forms.ImageField(widget=FileInputWidget, label=_('Иконка'))

    class Meta:
        model = Profile
        fields = ('icon',)
        widgets = {
            'icon': forms.ClearableFileInput(attrs={'label': _('Выберите файл')})
        }

