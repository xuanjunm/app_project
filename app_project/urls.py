from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.views.generic import TemplateView
admin.autodiscover()

# tastypie api purposes
from tastypie.api import Api
from events.api import EventResource
from patio.api import UserResource
v01_api = Api(api_name='v01')
v01_api.register(EventResource())
v01_api.register(UserResource())

urlpatterns = patterns('',
    url(r'^', include('patio.urls', namespace='patio')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^events/', include('events.urls', namespace='events')),
    url(r'^api/', include(v01_api.urls)),
)
