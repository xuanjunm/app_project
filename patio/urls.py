from . import views
from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView

urlpatterns = patterns('',
    url(r'^$', TemplateView.as_view(template_name='patio/main.html'), 
        name='main'),
    url(r'^login/$', 'django.contrib.auth.views.login',
        {'template_name': 'patio/login.html'}, name='login'),
    url(r'^logout/$', 'django.contrib.auth.views.logout',
        name='logout'),
       # {'next_page': '/'}, name='logout'),
    url(r'^dashboard/$', views.DashboardView.as_view(), name='dashboard'),
)
