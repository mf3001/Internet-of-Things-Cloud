from django.conf.urls import url

from . import views

urlpatterns = [
    #url(r'^\?source=(?P<source>[a-zA-Z0-9]+)&destination=(?P<destination>[a-zA-Z0-9]+)$', views.route_plan, name='route_plan'),
    url(r'^$', views.index, name='index'),
]