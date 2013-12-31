from django.conf.urls import patterns, url, include
#from api import EventResource, AccountResource
from events import views

urlpatterns = patterns('',
    url(r'^$', views.EventsList.as_view(), name='events_list'),
    url(r'^(?P<pk>\d+)/$', views.EventDetailsView.as_view(), name='event_details'),
    url(r'^create_event/$', views.CreateEventView.as_view(), name='create_event'),
    url(r'^update_event/(?P<pk>\d+)/$', views.UpdateEventView.as_view(), name='update_event'),
    url(r'^delete_event/(?P<pk>\d+)/$', views.DeleteEventView.as_view(), name='delete_event'),

)
