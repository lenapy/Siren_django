from django.conf.urls import url, include
from django.contrib import admin

from siren_proj import views
from siren_proj.user import urls as user_urls
from siren_proj.video import urls as video_urls

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^user/', include(user_urls, namespace='user')),
    url(r'^video/', include(video_urls, namespace='video')),
    url(r'^admin/', include(admin.site.urls))


]
