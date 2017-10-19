from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'my-vm/$', views.myVM),
    url(r'^vm-create/$', views.createVM),
    url(r'^account/$', views.accountInfo)
]