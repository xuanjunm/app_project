from tastypie.resources import ModelResource, ALL, ALL_WITH_RELATIONS
from tastypie.authentication import ApiKeyAuthentication, Authentication
from tastypie.authorization import Authorization, DjangoAuthorization
from tastypie import fields

from .models import *
from basal.api import *

class EventCustomAuthorization(Authorization):
    #def read_detail(self, object_list, bundle):
    #    return True

    def create_detail(self, object_list, bundle):
        if bundle.request.user == None:
            return False

        return True

    def update_list(self, object_list, bundle):
        return []

    def update_detail(self, object_list, bundle):
        #import pdb;pdb.set_trace()
        return bundle.obj.fk_event_poster_user == bundle.request.user

    def update_list(self, object_list, bundle):
        return []

    def delete_detail(self, object_list, bundle):
        return bundle.obj.fk_event_poster_user == bundle.request.user

class AddressResource(ModelResource):
    class Meta:
        queryset = Address.objects.all()

class EventResource(ModelResource):
    fk_event_poster_user = fields.ForeignKey(UserResource,
                                             'fk_event_poster_user',
                                             full=True)
    fk_address = fields.ForeignKey(AddressResource,
                                   'fk_address',
                                   full=True)

    class Meta:
        queryset = Event.objects.all()
        authentication = CustomAuthentication()
        authorization = EventCustomAuthorization()
        filtering = { 'event_title': 'contains',
                      'event_type': ALL,
                      'event_status': ALL,
                      'fk_event_poster_user': ALL_WITH_RELATIONS,
                    }
