from django.conf.urls.defaults import *
from django.views.generic.simple import direct_to_template

from django_restapi.model_resource import Collection
from django_restapi.responder import JSONResponder
from project.models import Project

from django.contrib import admin
admin.autodiscover()

project_resource = Collection(
    queryset = Project.objects.all(),
    responder = JSONResponder(),
)

urlpatterns = patterns('',
                       (r'^admin/', include(admin.site.urls)),
                       (r'^project/', include('project.urls')),
                       (r'^forum/', include('forum.urls')),
                       (r'^about/$', direct_to_template, {'template': 'about.html'}),
                       (r'^media/(?P<path>.*)$', 'django.views.static.serve',
                        {'document_root': '/home/rahuljha/step2/media/'}),
                       #REST interface
                       (r'^json/project/(.*?)/?$', project_resource),
)


