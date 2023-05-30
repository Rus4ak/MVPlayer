from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.forms.widgets import ClearableFileInput

from main.models import Profile


class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

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
    icon = forms.ImageField(widget=FileInputWidget)

    class Meta:
        model = Profile
        fields = ('icon',)
        widgets = {
            'icon': forms.ClearableFileInput(attrs={'label': ('Выберите файл')})
        }


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name')
