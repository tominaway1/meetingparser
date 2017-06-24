from django.conf.urls import include, url
from . import views

urlpatterns = [
    url(r'^$', views.identify, name='identify'),
    url(r'^profiles$', views.identify, name='profiles')
]