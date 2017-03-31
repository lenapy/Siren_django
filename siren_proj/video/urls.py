from django.conf.urls import url

from siren_proj.video import views

urlpatterns = [

    url(r'^tv_show/(?P<pk>[0-9]+)/$', views.tv_show_view, name='tv_show'),
    url(r'^film/(?P<pk>[0-9]+)/$', views.film_view, name='film'),
    url(r'^add/(?P<pk>[0-9]+)/$', views.subscribe, name='add'),
    url(r'^unsubscribe/(?P<pk>[0-9]+)/$', views.unsubscribe, name='unsubscribe'),
    url(r'^searching_result/$', views.search, name='search'),
    url(r'^main/$', views.main, name='main')

   ]