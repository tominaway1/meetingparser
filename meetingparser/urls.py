from django.conf.urls import include, url
from django.contrib import admin
import apps.audiohandler.views
import apps.texthandler.views
admin.autodiscover()

# Examples:
# url(r'^$', 'gettingstarted.views.home', name='home'),
# url(r'^blog/', include('blog.urls')),

urlpatterns = [
    url(r'^$', apps.audiohandler.views.index, name='index'),
    url(r'^audio/', include('apps.audiohandler.urls')),
    url(r'^twilio/', include('apps.twilio_app.urls')),
    url(r'text/(?P<audio_uuid>[0-9a-f-]+)', apps.texthandler.views.analyze_audio, name='read_text'),
    url(r'^admin/', include(admin.site.urls)),
]
