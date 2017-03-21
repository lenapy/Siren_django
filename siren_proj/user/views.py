from django.shortcuts import render, redirect
import uuid
from siren_proj import models
from siren_proj.user.forms import RegistrationForm, LoginForm, PasswordChangeForm
from siren_proj.models import User, Session


def index(request):
    videos = models.Video.objects.all()
    return render(request, 'index.html', {'videos': videos})


def registration(request):
    if request.method == 'POST':
        form = RegistrationForm(data=request.POST)
        if form.is_valid():
            if not User.objects.registration(
                form.cleaned_data['login'],
                form.cleaned_data['password'],
                form.cleaned_data['username'],
                form.cleaned_data['mail_address']
            ):
                pass
            return redirect('user:login')
    else:
        form = RegistrationForm()
    return render(request, 'user/registration.html',
                  context={'form': form})


def login(request):
    if request.method == 'POST':
        form = LoginForm(data=request.POST)
        if form.is_valid():
            session = Session.objects.create(user=form.user, token=uuid.uuid4())
            response = redirect('/')
            response.set_cookie('user-session', session.token,
                                expires=session.date_expired)
            return response
    else:
        form = LoginForm()

    return render(request, 'user/login.html', context={'form': form})


def logout(request):
    user_session = request.COOKIES['user-session']
    session = Session.objects.filter(token=user_session).last()
    if session.delete():
        return redirect('user:login')
    else:
        print("err")


def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(data=request.POST)
        if form.is_valid():
            new_pass = form.cleaned_data
            print(new_pass)
            User.objects.change_password(new_pass)
            return redirect('user:login')
        else:
            pass
    else:
        form = PasswordChangeForm()
    return render(request, 'user/change_password.html', context={'form': form})
