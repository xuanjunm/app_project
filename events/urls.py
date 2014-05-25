from django.conf.urls import patterns, url, include
from . import views

urlpatterns = patterns('',
    url(r'^$', views.EventListView.as_view(), name='event_list'),
    url(r'^(?P<pk>\d+)/$', views.EventDetailView.as_view(), 
        name='event_detail'),
    url(r'^event_create/$', views.EventCreateView.as_view(), 
        name='event_create'),
    url(r'^event_update/(?P<pk>\d+)/$', views.EventUpdateView.as_view(), 
        name='event_update'),
    url(r'^event_delete/(?P<pk>\d+)/$', views.EventDeleteView.as_view(), 
        name='event_delete'),
    url(r'^event_comment_create/(?P<pk>\d+)/$', views.event_comment_create, name='event_comment_create'),
    url(r'^event_rsvp/(?P<pk>\d+)/$', views.event_rsvp, name='event_rsvp'),
    url(r'^event_rsvp_remove/(?P<pk>\d+)/$', 
        views.event_rsvp_remove, name='event_rsvp_remove'),
)
