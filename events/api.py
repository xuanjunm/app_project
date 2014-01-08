from tastypie.resources import ModelResource, ALL, ALL_WITH_RELATIONS
from tastypie.authorization import Authorization
from tastypie import fields

from .models import *
from basal.api import *

class EventResource(ModelResource):
    fk_event_poster_user = fields.ForeignKey(UserResource,
                                           'fk_event_poster_user',
                                           full=True)

    class Meta:
        queryset = Event.objects.all()
        # not exactly necessary, leaving it here to keep readable
        resource_name = 'event'

        authorization = Authorization()
        allowed_methods = ['get']
     #   filtering = { 'event_time': ALL,
    #                  'event_create_time': ALL,
     #                 'event_location': ALL,
     #                 'event_name': 'contains',
     #                 'event_status': ALL,
#                      'event_organizer_id': ALL_WITH_RELATIONS,
     #                 'event_type': ALL}
