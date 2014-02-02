from tastypie.resources import ModelResource
from tastypie.authorization import Authorization
from tastypie.authentication import ApiKeyAuthentication
from tastypie.exceptions import Unauthorized
from tastypie import fields
from tastypie.constants import ALL

from django.contrib.auth.models import User
from .models import *

from tastypie.http import HttpUnauthorized

#class CustomAuthentication(ApiKeyAuthentication):
#    def is_authenticated(self, request, **kwargs):
#        """
#        Will try to authenticate User using ApiKey
#        If fail, User = None
#        """
#
#        from tastypie.compat import User
#
#        try:
#            username, api_key = self.extract_credentials(request)
#        except ValueError:
#            request.user = None
#            return True
#        #return self._unauthorized()
#
#        if not username or not api_key:
#            request.user = None
#            return True
#        #return self._unauthorized()
#
#        try:
#            #import pdb;pdb.set_trace()
#            user = User.objects.get(username=username)
#        except (User.DoesNotExist, User.MultipleObjectsReturned):
#            request.user = None
#            return True
#        #  return self._unauthorized()
#
#        if not self.check_active(user):
#            request.user = None
#            return True
#
#        key_auth_check = self.get_key(user, api_key)
#        if key_auth_check and not isinstance(key_auth_check, 
#                                             HttpUnauthorized):
#            request.user = user
#        else:
#            request.user = None
#
#        return True
#
#class UserCustomAuthorization(Authorization):
#    def read_list(self, object_list, bundle):
##       import pdb;pdb.set_trace()
#       return object_list
#
#    def read_detail(self, object_list, bundle):
#       return bundle.obj == bundle.request.user 
#
#    def create_detail(self, object_list, bundle):
#        return Unauthorized('Sorry no create_detail')
#
#    def update_list(self, object_list, bundle):
#        return Unauthorized('Sorry, no update list')
#
#    def update_detail(self, object_list, bundle):
#        return bundle.obj == bundle.request.user
#
#    def delete_detail(self, object_list, bundle):
#        return Unauthorized('Sorry, no deletes')
#
#    def delete_list(self, object_list, bundle):
#        return Unauthorized('Sorry, no deletes')
#
#class UserProfileCustomAuthorization(Authorization):
#    def read_list(self, object_list, bundle):
#        return []
#
#    def read_detail(self, object_list, bundle):
#       #import pdb;pdb.set_trace()
#       return bundle.obj.user == bundle.request.user 
#
#    def create_detail(self, object_list, bundle):
#        return Unauthorized('Sorry no create_detail')
#
#    def update_list(self, object_list, bundle):
#        return Unauthorized('Sorry, no update list')
#
#    def update_detail(self, object_list, bundle):
#        return bundle.obj.user == bundle.request.user
#
#    def delete_detail(self, object_list, bundle):
#        return Unauthorized('Sorry, no deletes')
#
#    def delete_list(self, object_list, bundle):
#        return Unauthorized('Sorry, no deletes')
#
#
#class UserProfileResource(ModelResource):
#    class Meta:
#        queryset = UserProfile.objects.all()
#        authentication = CustomAuthentication()
#        authorization = UserProfileCustomAuthorization()
#
#    def dehydrate(self, bundle):
#        self.fields['user_description'].use_in = u'detail'
#        return bundle
#
#class UserResource(ModelResource):
#    profile = fields.OneToOneField(UserProfileResource, 'profile', full=True)
#
#    class Meta:
#        queryset = User.objects.all()
#        authentication = CustomAuthentication()
#        authorization = UserCustomAuthorization()
#        excludes = ['password', 'is_staff', 'is_active', 'is_superuser']
#        filtering = { 'username': ALL }
#
##        import pdb;pdb.set_trace()
#    def dehydrate(self, bundle):
#        self.fields['username'].use_in = u'detail'
#        self.fields['email'].use_in = u'detail'
#        self.fields['date_joined'].use_in = u'detail'
#        self.fields['last_login'].use_in = u'detail'
#        self.fields['id'].use_in = u'detail'
#        return bundle
#
#
###
