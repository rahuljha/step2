from django.conf.urls.defaults import *
from django.views.generic import list_detail
from django.views.generic.simple import direct_to_template
from project.models import project
from settings import WORKSPACE_DIR

from django.contrib import adminadmin.autodiscover()


urlpatterns = patterns('',
                       (r'^$', direct_to_template, {'template': 'home.html'}),
                       (r'^home/$', direct_to_template, {'template': 'home.html'}),
                       (r'^about/$', direct_to_template, {'template': 'about.html'}),
                       (r'^admin/', include(admin.site.urls)),
                       (r'^projects/', include('project.urls')),
                       (r'^forum/', include('forum.urls')),
                       (r'^site_media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': WORKSPACE_DIR + '/site_media/'}),
                       #REST interface                       (r'^api/', include('api.urls')))
