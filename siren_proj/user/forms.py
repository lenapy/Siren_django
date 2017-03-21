from django import forms
from django.contrib.auth.hashers import check_password
from siren_proj.models import User


class RegistrationForm(forms.Form):
    username = forms.CharField(max_length=50, initial='')
    mail_address = forms.EmailField(initial='')
    login = forms.CharField(max_length=50, initial='')
    password = forms.CharField(min_length=6, initial='')

    def clean_login(self):
        login = self.cleaned_data['login']
        if User.objects.filter(login=login).first():
            raise forms.ValidationError('login %s already exist' % login)
        return login


class LoginForm(forms.Form):
    login = forms.CharField(max_length=50, initial='')
    password = forms.CharField(min_length=6, initial='')

    def clean(self):
        cleaned_data = super().clean()
        login = cleaned_data['login']
        password = cleaned_data['password']
        self.user = User.objects.filter(login=login).first()
        if not (self.user and check_password(password, self.user.password)):
            raise forms.ValidationError('Incorrect login or password')
        return login


class PasswordChangeForm(forms.Form):
    password = forms.CharField(min_length=6, initial='')
    new_password = forms.CharField(min_length=6, initial='')
    reenter_password = forms.CharField(min_length=6, initial='')

    def clean(self):
        cleaned_data = super().clean()
        login = cleaned_data.get('login')
        password = cleaned_data['password']
        new_password = cleaned_data['new_password']
        reenter_password = cleaned_data['reenter_password']
        self.user = User.objects.filter(login=login).first()
        if self.user and new_password != reenter_password or new_password == password:
            raise forms.ValidationError('Incorrect password')
        return new_password