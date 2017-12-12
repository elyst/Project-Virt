from django.conf.urls import url, include
from django.contrib import admin
from django.contrib.auth import views as auth_views



from . import views

urlpatterns = [
    url(r'^$', views.custom_login, name='login'),
    url(r'^register/$', views.signUpRequest, name='signUpRequest'),
    url(r'^password_reset/$', auth_views.password_reset, name='password_reset'),
    url(r'^password_reset/done/$', auth_views.password_reset_done, name='password_reset_done'),
    url(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        auth_views.password_reset_confirm, name='password_reset_confirm'),
    url(r'^reset/done/$', auth_views.password_reset_complete, name='password_reset_complete'),
    
]