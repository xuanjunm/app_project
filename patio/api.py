from tastypie.resources import ModelResource
from tastypie import fields
from tastypie.constants import ALL

from django.contrib.auth.models import User

class UserResource(ModelResource):
    nickname = fields.CharField(attribute='profile__user_nickname')
    gender = fields.CharField(attribute='profile__user_gender')
    description = fields.CharField(attribute='profile__user_description')

    class Meta:
        queryset = User.objects.all()
        # not exactly necessary, leaving it here to keep readable
        resource_name = 'user'

        excludes = ['password', 'is_staff', 'is_active', 'is_superuser']
        allowed_methos = ['get']
        #        filtering = { 'user_user_name': ALL }



