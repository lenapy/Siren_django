from django.conf.urls import url, include
from django.contrib import admin

from siren_proj import views
from siren_proj.user import urls as user_urls

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^user/', include(user_urls, namespace='user')),
    url(r'^admin/', include(admin.site.urls))


]
