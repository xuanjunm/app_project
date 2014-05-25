from tastypie.resources import ModelResource, ALL, ALL_WITH_RELATIONS
from tastypie.authentication import ApiKeyAuthentication, Authentication
from tastypie.authorization import Authorization, DjangoAuthorization
from tastypie import fields
from tastypie.exceptions import Unauthorized, BadRequest

from .models import *
from basal.api import *

class EventRSVPCustomAuthorization(CustomAuthorization):
    def create_detail(self, object_list, bundle):
        if bundle.request.user == None:
            return Unauthorized('Disabled')
        return True

    def read_detail(self, object_list, bundle):
        return bundle.obj.fk_user == bundle.request.user

    def update_detail(self, object_list, bundle):
        return bundle.obj.fk_user == bundle.request.user

    def delete_detail(self, object_list, bundle):
#        import pdb; pdb.set_trace()
        return bundle.obj.fk_user == bundle.request.user

class EventCustomAuthorization(CustomAuthorization):
    def create_detail(self, object_list, bundle):
        if bundle.request.user == None:
            return False
        return True

    def read_detail(self, object_list, bundle):
        return True

    def update_detail(self, object_list, bundle):
        return bundle.obj.fk_event_poster_user == bundle.request.user

    def delete_detail(self, object_list, bundle):
        return bundle.obj.fk_event_poster_user == bundle.request.user

class EventImageResource(ModelResource):
    class Meta:
        queryset = EventImage.objects.all()
        excludes = ['id']

class EventLikeResource(ModelResource):
    fk_event = fields.ForeignKey('events.api.EventResource', 'fk_event')
    fk_user = fields.ForeignKey(UserResource, 'fk_user', full=True) 
    class Meta:
        queryset = EventLike.objects.all()
        filtering = { 'fk_event': ALL,
                      'fk_user': ALL,
                    }
        authentication = CustomAuthentication()
        authorization = EventRSVPCustomAuthorization()

    def obj_create(self, bundle, **kwargs):
        try:
#            import pdb;pdb.set_trace()
            user = UserResource().get_via_uri(bundle.data['fk_user'], bundle.request)
            event = EventResource().get_via_uri(bundle.data['fk_event'], bundle.request)
            EventLike.objects.filter(fk_event=event).get(fk_user=user)

        except EventLike.DoesNotExist:
            bundle = super(EventLikeResource, self).obj_create(bundle, **kwargs)

        else:
            raise BadRequest('Like already.')

        return bundle

class EventCommentResource(ModelResource):
    fk_comment_poster_user = fields.ForeignKey(UserResource, 'fk_comment_poster_user')

    class Meta:
        queryset = EventComment.objects.all()
        authentication = CustomAuthentication()
        authorization = EventRSVPCustomAuthorization()
        filtering = { 'comment_detail': 'contains',
                      'fk_event':ALL,
                      'comment_post_time':ALL,
                      'fk_comment_poster_user': ALL,
                    }
        excludes = ['id']
    def dehydrate(self, bundle):
#        import pdb;pdb.set_trace()
        bundle.data['fk_comment_poster_user_name'] = bundle.obj.fk_comment_poster_user.username
        return bundle

class EventRSVPResource(ModelResource):
    fk_event = fields.ForeignKey('events.api.EventResource', 'fk_event')
    fk_user = fields.ForeignKey(UserResource, 'fk_user')
                                
    class Meta:
        queryset = EventRSVP.objects.all()
        excludes = ['id']
        authentication = CustomAuthentication()
        authorization = EventRSVPCustomAuthorization()
        
    def obj_create(self, bundle, **kwargs):
        try:
#            import pdb;pdb.set_trace()
            user = UserResource().get_via_uri(bundle.data['fk_user'], bundle.request)
            event = EventResource().get_via_uri(bundle.data['fk_event'], bundle.request)
            EventRSVP.objects.filter(fk_event=event).get(fk_user=user)

        except EventRSVP.DoesNotExist:
            bundle = super(EventRSVPResource, self).obj_create(bundle, **kwargs)

        else:
            raise BadRequest('RSVP already.')

        return bundle

class EventResource(ModelResource):
    fk_event_poster_user = fields.ForeignKey(UserResource, 'fk_event_poster_user')
    event_image = fields.ToManyField(EventImageResource, 'event_image',full=True, null=True)
    event_comment = fields.ToManyField(EventCommentResource, 'event_comment',full=True, null=True)

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

    def dehydrate(self, bundle):
        bundle.data['event_rsvp_count'] = Event.objects.get(id=bundle.obj.id).get_event_rsvp_count()
        bundle.data['event_like_count'] = Event.objects.get(id=bundle.obj.id).get_event_like_count()
        bundle.data['fk_event_poster_user_name'] = bundle.obj.fk_event_poster_user.username
        return bundle
