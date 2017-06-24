from django.conf.urls import include, url
from django.contrib import admin
import apps.audiohandler.views

admin.autodiscover()

# Examples:
# url(r'^$', 'gettingstarted.views.home', name='home'),
# url(r'^blog/', include('blog.urls')),

urlpatterns = [
    url(r'^$', apps.audiohandler.views.index, name='index'),
    url(r'^audio/', include('apps.audiohandler.urls')),
    url(r'^admin/', include(admin.site.urls)),
]
