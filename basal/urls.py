from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView

from . import views

# for tastypie web service
#from .api import * 
#user_resource = UserResource()

urlpatterns = patterns('',
    url(r'^$', TemplateView.as_view(template_name='basal/main.html'), 
        name='main'),
    url(r'^user_login/$', 'django.contrib.auth.views.login',
        {'template_name': 'basal/login.html'}, name='user_login'),
    url(r'^logout/$', 'django.contrib.auth.views.logout',
        name='logout'),
    url(r'^user_create/$', views.UserCreateView.as_view(), name='user_create'),
    url(r'^user_update/$', views.UserUpdateView.as_view(), name='user_update'),
    url(r'^dashboard/$', views.DashboardView.as_view(), name='dashboard'),
    url(r'^address_detail/(?P<pk>\d+)/$', views.AddressDetailView.as_view(), 
        name='address_detail'),
    url(r'^address_create/$', views.AddressCreateView.as_view(), 
        name='address_create'),
    url(r'^address_update/(?P<pk>\d+)/$', views.AddressUpdateView.as_view(), 
        name='address_update'),
#    url(r'^api/', include(user_resource.urls)),
)
