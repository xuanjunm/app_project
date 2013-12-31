from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView

from . import views

# for tastypie web service
#from .api import * 
#user_resource = UserResource()

urlpatterns = patterns('',
    url(r'^$', TemplateView.as_view(template_name='patio/main.html'), 
        name='main'),
    url(r'^login/$', 'django.contrib.auth.views.login',
        {'template_name': 'patio/login.html'}, name='login'),
    url(r'^logout/$', 'django.contrib.auth.views.logout',
        name='logout'),
    url(r'^register/$', views.CreateUser.as_view(), name='create_user'),
    url(r'^dashboard/$', views.DashboardView.as_view(), name='dashboard'),
#    url(r'^api/', include(user_resource.urls)),
)
