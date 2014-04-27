from tastypie.resources import ModelResource
from tastypie.authorization import Authorization
from tastypie.authentication import ApiKeyAuthentication, BasicAuthentication
from tastypie.exceptions import Unauthorized,BadRequest
from tastypie import fields
from tastypie.constants import ALL
from tastypie.models import ApiKey
from django.db import IntegrityError

from .models import *

from tastypie.http import HttpUnauthorized
from django.contrib.auth import get_user_model

class CustomAuthentication(ApiKeyAuthentication):
    def is_authenticated(self, request, **kwargs):
        """
        Will try to authenticate User using ApiKey
        If fail, User = None
        """
        User = get_user_model()
        try:
            username, api_key = self.extract_credentials(request)
        except ValueError:
            request.user = None
            # user = None, but can still access api
            return True 
#            return self._unauthorized()

        if not username or not api_key:
            request.user = None
            # user = None, but can still access api
            return True
#            return self._unauthorized()

        try:
            #import pdb;pdb.set_trace()
            user = User.objects.get(username=username)
        except (User.DoesNotExist, User.MultipleObjectsReturned):
            request.user = None
            # user = None, but can still access api
            return True
#            return self._unauthorized()

        if not self.check_active(user):
            request.user = None
            return True

        key_auth_check = self.get_key(user, api_key)
        if key_auth_check and not isinstance(key_auth_check, 
                HttpUnauthorized):
            request.user = user
        else:
            request.user = None

        return True

class UserCustomAuthorization(Authorization):
    def create_list(self, object_list, bundle):
        return True

    def read_list(self, object_list, bundle):
        #       import pdb;pdb.set_trace()
        return object_list

    def update_list(self, object_list, bundle):
        return Unauthorized('Disabled')

    def delete_list(self, object_list, bundle):
        return Unauthorized('Disabled')

    def create_detail(self, object_list, bundle):
        return True
 
    def read_detail(self, object_list, bundle):
        return bundle.obj == bundle.request.user 

    def update_detail(self, object_list, bundle):
        return bundle.obj == bundle.request.user

    def delete_detail(self, object_list, bundle):
        return Unauthorized('Disabled')

class PropertiesCustomAuthorization(Authorization):
    def create_list(self, object_list, bundle):
        return Unauthorized('Disabled')

    def read_list(self, object_list, bundle):
        return object_list.filter(fk_user=bundle.request.user)

    def update_list(self, object_list, bundle):
        return Unauthorized('Disabled')

    def delete_list(self, object_list, bundle):
        return Unauthorized('Disabled')

    def create_detail(self, object_list, bundle):
        if bundle.request.user == None:
            return False
        return True

    def read_detail(self, object_list, bundle):
        return bundle.obj.fk_user == bundle.request.user

    def update_detail(self, object_list, bundle):
        #import pdb;pdb.set_trace()
        return bundle.obj.fk_user == bundle.request.user

    def delete_detail(self, object_list, bundle):
        return bundle.obj.fk_user == bundle.request.user

class UserImageResource(ModelResource):
    class Meta:
        queryset = UserImage.objects.all()
        authentication = CustomAuthentication()
        authorization = PropertiesCustomAuthorization()
        filtering = { 'fk_user': ALL,
                        'path': ALL},

class UserResource(ModelResource):
    fk_user_image = fields.ForeignKey(UserImageResource,
                                      'fk_user_image',
                                      full=True, null=True)

    fk_user_background_image = fields.ForeignKey(UserImageResource,
                               'fk_user_background_image',
                               full=True, null=True)

    class Meta:
        queryset = CustomUser.objects.all()
        authentication = CustomAuthentication()
        authorization = UserCustomAuthorization()
        excludes = ['password', 'is_staff', 'is_active', 'is_superuser']
        filtering = { 'username': ALL }

    def dehydrate(self, bundle):
        self.fields['username'].use_in = u'detail'
        self.fields['email'].use_in = u'detail'
        self.fields['date_joined'].use_in = u'detail'
        self.fields['last_login'].use_in = u'detail'
#        self.fields['id'].use_in = u'detail'
        return bundle

    def obj_create(self, bundle, **kwargs):
        try:
            bundle = super(UserResource, self).obj_create(bundle, **kwargs)
            bundle.obj.set_password(bundle.data.get('password'))
            bundle.obj.save() 
        except IntegrityError:

            usernamelist=[user.username for user in CustomUser.objects.all()]
            if bundle.data['username'] in usernamelist:
                raise BadRequest('Username -'+bundle.data['username']+'- has been used.')
            emaillist=[user.email for user in CustomUser.objects.all()]
            if bundle.data['email'] in emaillist:
                raise BadRequest('Email -'+bundle.data['email']+'- has been used.')
        return bundle

class AddressResource(ModelResource):
    fk_user = fields.ForeignKey(UserResource,
                                 'fk_user')
    class Meta:
        queryset = Address.objects.all()
        authentication = CustomAuthentication()
        authorization = PropertiesCustomAuthorization()

class ApiTokenResource(ModelResource):
    user = fields.ForeignKey(UserResource,
                             'user',
                             full=True)

    class Meta:
        queryset = ApiKey.objects.all()
        resource_name = 'token'
        include_resource_uri = False
        fields = ['key']
        list_allowed_methods = []
        detail_allowed_methids = ['get']
        authentication = BasicAuthentication()

    def get_detail(self, request, **kwargs):
        #        import pdb;pdb.set_trace()
#        if kwargs['pk'] != 'auth':
           # raise NotImplementedError('Resource not found')
        obj = ApiKey.objects.get(user=request.user)

        bundle = self.build_bundle(obj=obj, request=request)
        bundle = self.full_dehydrate(bundle)
        bundle = self.alter_detail_data_to_serialize(request, bundle)
        return self.create_response(request, bundle)
