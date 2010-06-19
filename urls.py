from django.conf.urls.defaults import *
from django.views.generic.simple import direct_to_template

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
                       (r'^admin/', include(admin.site.urls)),
                       (r'^forum/', include('forum.urls')),
                       (r'^about/$', direct_to_template, {'template': 'about.html'}),
                       (r'^media/(?P<path>.*)$', 'django.views.static.serve',
                        {'document_root': '/Users/rahuljha/source_code/step2/media/'}),

)
