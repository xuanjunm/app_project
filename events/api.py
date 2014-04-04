from tastypie.resources import ModelResource, ALL, ALL_WITH_RELATIONS
from tastypie.authentication import ApiKeyAuthentication, Authentication
from tastypie.authorization import Authorization, DjangoAuthorization
from tastypie import fields
from tastypie.exceptions import Unauthorized

from .models import *
from basal.api import *

class EventRSVPCustomAuthorization(Authorization):
    def create_list(self, object_list, bundle):
        return Unauthorized('Disabled')

    def read_list(self, object_list, bundle):
        return object_list
#        return object_list.filter(fk_user=bundle.request.user)

    def update_list(self, object_list, bundle):
        return Unauthorized('Disabled')

    def delete_list(self, object_list, bundle):
        return Unauthorized('Disabled')

    def create_detail(self, object_list, bundle):
        if bundle.request.user == None:
            return False
        return True

    def read_detail(self, object_list, bundle):
        return True
#        return bundle.obj.fk_user == bundle.request.user

    def update_detail(self, object_list, bundle):
        #import pdb;pdb.set_trace()
        return bundle.obj.fk_user == bundle.request.user

    def delete_detail(self, object_list, bundle):
        return bundle.obj.fk_user == bundle.request.user

class EventCustomAuthorization(Authorization):
    def create_list(self, object_list, bundle):
        return Unauthorized('Disabled')

    def read_list(self, object_list, bundle):
#        import pdb;pdb.set_trace()
        return object_list

    def update_list(self, object_list, bundle):
        return Unauthorized('Disabled')

    def delete_list(self, object_list, bundle):
        return Unauthorized('Disabled')

    def create_detail(self, object_list, bundle):
        if bundle.request.user == None:
            return False
        return True

    def read_detail(self, object_list, bundle):
        return True

    def update_detail(self, object_list, bundle):
        #import pdb;pdb.set_trace()
        return bundle.obj.fk_event_poster_user == bundle.request.user

    def delete_detail(self, object_list, bundle):
        return bundle.obj.fk_event_poster_user == bundle.request.user

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
        ordering = ['event_date', 'event_time', 'event_create_time',
                    'event_view_count', 'event_rsvp', 'event_like']
        filtering = { 'event_title': 'contains',
                      'event_date': ALL,
                      'event_type': ALL,
                      'event_status': ALL,
                      'fk_event_poster_user': ALL_WITH_RELATIONS,
                    }

class EventRSVPResource(ModelResource):
    fk_event = fields.ForeignKey(EventResource,
                                 'fk_event')
    fk_user = fields.ForeignKey(UserResource,
                                 'fk_user',
                                 full=True)
    class Meta:
        queryset = EventRSVP.objects.all()
        filtering = { 'fk_event': ALL,
                      'fk_user': ALL,
                    }
        authentication = CustomAuthentication()
        authorization = EventRSVPCustomAuthorization()

class EventLikeResource(ModelResource):
    fk_event = fields.ForeignKey(EventResource,
                                 'fk_event')
    fk_user = fields.ForeignKey(UserResource,
                                 'fk_user',
                                 full=True)
    class Meta:
        queryset = EventLike.objects.all()
        filtering = { 'fk_event': ALL,
                      'fk_user': ALL,
                    }
        authentication = CustomAuthentication()
        authorization = EventRSVPCustomAuthorization()


