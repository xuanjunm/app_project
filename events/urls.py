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
    url(r'^update_event/(?P<pk>\d+)/$', views.UpdateEventView.as_view(), 
        name='update_event'),
    url(r'^delete_event/(?P<pk>\d+)/$', views.DeleteEventView.as_view(), 
        name='delete_event'),
#    url(r'^api/', include(event_resource.urls)),
)
