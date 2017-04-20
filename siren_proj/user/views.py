from django.shortcuts import render, redirect
import uuid
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from siren_proj import models
from siren_proj.user.forms import RegistrationForm, LoginForm, PasswordChangeForm
from siren_proj.models import User, Session, Video


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
            response = redirect('user:profile')
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
            new_pass = form.cleaned_data['new_password']
            User.objects.change_password(new_pass, request.user.id)
            return redirect('user:login')
        else:
            pass
    else:
        form = PasswordChangeForm()
    return render(request, 'user/change_password.html', context={'form': form})


def profile(request):
    videos = Video.objects.filter(usersubscription__user_id=request.user.id).order_by('year_of_issue').reverse()
    info_web = models.Website.objects.all()
    paginator = Paginator(videos, 9)
    page = request.GET.get('page')
    try:
        videos = paginator.page(page)
    except PageNotAnInteger:
        videos = paginator.page(1)
    except EmptyPage:
        videos = paginator.page(paginator.num_pages)

    return render(request, 'user/profile.html', {'videos': videos,
                                                 'info_web': info_web})


