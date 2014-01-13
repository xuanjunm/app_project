from django.conf.urls import patterns, url, include
from events import views

# for tastypie web service
#from .api import EventResource
#event_resource = EventResource()

urlpatterns = patterns('',
    url(r'^$', views.EventList.as_view(), name='event_list'),
    url(r'^(?P<pk>\d+)/$', views.EventDetailView.as_view(), 
        name='event_detail'),
    url(r'^event_create/$', views.EventCreateView.as_view(), 
        name='event_create'),
    url(r'^event_update/(?P<pk>\d+)/$', views.EventUpdateView.as_view(), 
        name='event_update'),
    url(r'^event_delete/(?P<pk>\d+)/$', views.EventDeleteView.as_view(), 
        name='event_delete'),
    url(r'^address_detail/(?P<pk>\d+)/$', views.AddressDetailView.as_view(), 
        name='address_detail'),
    url(r'^address_create/$', views.AddressCreateView.as_view(), 
        name='address_create'),
    url(r'^address_update/(?P<pk>\d+)/$', views.AddressUpdateView.as_view(), 
        name='address_update'),

#    url(r'^api/', include(event_resource.urls)),
)
