from django.conf.urls import url
from django.views.generic import TemplateView
from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^contact/$', views.contact),
    url(r'^pricing/$', views.pricing),
]