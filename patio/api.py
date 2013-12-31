from tastypie.resources import ModelResource
from tastypie import fields
from tastypie.constants import ALL
from django.contrib.auth.models import User
from .models import UserProfile

#class UserResource(ModelResource):
#    class Meta:
#        queryset = User.objects.all()
#        resource_name = 'user'
#        excludes = ['user_password', 'user_type',
#                    'user_register_date', 'user_image']
#        filtering = { 'user_user_name': ALL }
