from tastypie.resources import ModelResource, ALL, ALL_WITH_RELATIONS
from tastypie.authorization import Authorization

from tastypie import fields
from models import Event
from accounts.api import AccountResource

class EventResource(ModelResource):
    event_organizer_id = fields.ForeignKey(AccountResource,
                                           'event_organizer_id',
                                           full=True)

    class Meta:
        queryset = Event.objects.all()
        resource_name = 'event'
        authorization = Authorization()
        filtering = { 'event_time': ALL,
                      'event_create_time': ALL,
                      'event_location': ALL,
                      'event_name': 'contains',
                      'event_status': ALL,
                      'event_organizer_id': ALL_WITH_RELATIONS,
                      'event_type': ALL}
