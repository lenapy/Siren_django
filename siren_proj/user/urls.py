from django.conf.urls import url

from siren_proj.user import views

urlpatterns = [

    url(r'^registration/$', views.registration, name='registration'),
    url(r'^login/$', views.login, name='login'),
    url(r'^logout/$', views.logout, name='logout'),
    url(r'^change_password/$', views.change_password, name='change_password'),

]