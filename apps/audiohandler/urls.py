from django.conf.urls import include, url
from . import views

urlpatterns = [
    url(r'^$', views.identify, name='identify'),
    url(r'^profiles$', views.get_all_profile, name='profiles'),
    url(r'^(?P<audio_uuid>[0-9a-f-]+)/split$',views.split_audio_file, name='split_audio'),
    url(r'^(?P<audio_uuid>[0-9a-f-]+)/identify$',views.identify_audio_file, name='identify_audio')
]
