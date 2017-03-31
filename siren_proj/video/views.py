from django.shortcuts import render, redirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import get_object_or_404

from siren_proj import models
from siren_proj.video.forms import SearchForm


def film_view(request, pk):
    film = models.Video.objects.filter(id=pk)
    return render(request, 'video/films.html', {'film': film})


def tv_show_view(request, pk):
    tv_shows = models.Video.objects.filter(id=pk)
    info_web = models.Website.objects.filter(video_id=pk)
    subscriptions = models.UserSubscription.objects.all()
    return render(request, 'video/tv_show.html', {'tv_shows': tv_shows,
                                                  'subscriptions': subscriptions,
                                                  'info_web': info_web})


def main(request):
    videos = models.Video.objects.all().distinct('name')
    subscriptions = models.UserSubscription.objects.all()
    paginator = Paginator(videos, 9)
    page = request.GET.get('page')
    try:
        videos = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        videos = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        videos = paginator.page(paginator.num_pages)

    return render(request, 'video/main.html', {'videos': videos,
                                               'subscriptions': subscriptions})


def subscribe(request, pk):
    is_user_subscribe = models.UserSubscription.objects.filter(video_id=pk).first()
    if is_user_subscribe:
        pass
    else:
        user_subscribe = models.UserSubscription.objects.create(user_id=request.user.id,
                                                                video_id=pk)
        user_subscribe.save()
    return redirect('video:main')


def unsubscribe(request, pk):
    user_subscribe = models.UserSubscription.objects.filter(user_id=request.user.id,
                                                            video_id=pk).first()
    if user_subscribe:
        models.UserSubscription.objects.filter(user_id=request.user.id,
                                               video_id=pk).delete()
    return redirect('video:main')


def search(request):
        form = SearchForm(data=request.POST)
        if form.is_valid():
            video_title = form.cleaned_data['video_title']
            videos = models.Video.objects.filter(name__icontains=video_title)
            paginator = Paginator(videos, 9)
            page = request.GET.get('page')
            try:
                videos = paginator.page(page)
            except PageNotAnInteger:
                videos = paginator.page(1)
            except EmptyPage:
                videos = paginator.page(paginator.num_pages)
            return render(request, 'video/searching_result.html', {'videos': videos})



