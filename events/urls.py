from django.conf.urls import patterns, url, include
from events import views

# for tastypie web service
#from .api import EventResource
#event_resource = EventResource()

urlpatterns = patterns('',
    url(r'^$', views.EventsList.as_view(), name='events_list'),
    url(r'^(?P<pk>\d+)/$', views.EventDetailsView.as_view(), 
        name='event_details'),
    url(r'^event_create/$', views.EventCreateView.as_view(), 
        name='event_create'),
    url(r'^event_update/(?P<pk>\d+)/$', views.EventUpdateView.as_view(), 
        name='event_update'),
    url(r'^event_delete/(?P<pk>\d+)/$', views.EventUpdateView.as_view(), 
        name='event_delete'),
#    url(r'^api/', include(event_resource.urls)),
)
