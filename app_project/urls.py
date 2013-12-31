from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.views.generic import TemplateView

from events.api import EventResource
#from patio.api import AccountResource
from tastypie.api import Api

v01_api = Api(api_name='v01')
#v01_api.register(AccountResource())
v01_api.register(EventResource())

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', TemplateView.as_view(template_name="main.html"), name="main"),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^events/', include('events.urls', namespace="events")),
    url(r'^api/', include(v01_api.urls)),
)
