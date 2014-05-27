from tastypie.resources import ModelResource, ALL, ALL_WITH_RELATIONS
from tastypie.authentication import ApiKeyAuthentication, Authentication
from tastypie.authorization import Authorization, DjangoAuthorization
from tastypie import fields
from tastypie.exceptions import Unauthorized,BadRequest

from .models import *
from basal.api import *

class DuplicateError(Exception):
  pass;

class EventRSVPCustomAuthorization(CustomAuthorization):
    def create_detail(self, object_list, bundle):
        if bundle.request.user == None:
            return Unauthorized('Disabled')
        return True

    def update_detail(self, object_list, bundle):
        #import pdb;pdb.set_trace()
        return bundle.obj.fk_user == bundle.request.user

    def delete_detail(self, object_list, bundle):
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

class EventCommentResource(ModelResource):
    fk_comment_poster_user = fields.ForeignKey(UserResource,
                                             'fk_comment_poster_user',
                                             full=True)

    fk_event = fields.ForeignKey('events.api.EventResource', 'fk_event')

    class Meta:
        queryset = EventComment.objects.all()

class EventRSVPResource(ModelResource):
    fk_event = fields.ForeignKey('events.api.EventResource', 'fk_event')
    fk_user = fields.ForeignKey(UserResource, 'fk_user', full=True)
                                
    class Meta:
        queryset = EventRSVP.objects.all()
        filtering = { 'fk_event': ALL,
                      'fk_user': ALL,
                    }
        authentication = CustomAuthentication()
        authorization = EventRSVPCustomAuthorization()
        
    def obj_create(self, bundle, **kwargs):
        try:
          user=UserResource().get_via_uri(bundle.data['fk_user'],bundle.request)
          event=EventResource().get_via_uri(bundle.data['fk_event'],bundle.request)
          userlist=[rsvp.fk_user for rsvp in EventRSVP.objects.filter(fk_event=event)]
          if user in userlist:
            raise DuplicateError
          bundle = super(EventRSVPResource, self).obj_create(bundle, **kwargs)
            
            # event=Event.objects.get(pk=bundle.)

        except DuplicateError:
          raise BadRequest('RSVP already.')
            # usernamelist=[user.username for user in CustomUser.objects.all()]
            # if bundle.data['username'] in usernamelist:
            #     raise BadRequest('Username -'+bundle.data['username']+'- has been used.')
            # emaillist=[user.email for user in CustomUser.objects.all()]
            # if bundle.data['email'] in emaillist:
            #     raise BadRequest('Email -'+bundle.data['email']+'- has been used.')
        # event=Event.objects.get(pk=bundle.obj.fk_event_id)
        event.event_rsvp=len(EventRSVP.objects.filter(fk_event__id=event.id))
        event.save()
        return bundle

    def obj_delete_like(self,bundle,**kwargs):
        # import pdb
        # pdb.set_trace()
        user=UserResource().get_via_uri(bundle.data['fk_user'],bundle.request)
        event=EventResource().get_via_uri(bundle.data['fk_event'],bundle.request)
        rsvplist=EventRSVP.objects.filter(fk_event=event,fk_user=user)
        rsvplist.delect()
        return bundle

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
          user=UserResource().get_via_uri(bundle.data['fk_user'],bundle.request)
          event=EventResource().get_via_uri(bundle.data['fk_event'],bundle.request)
          userlist=[like.fk_user for like in EventLike.objects.filter(fk_event=event)]
          if user in userlist:
            raise DuplicateError
          bundle = super(EventLikeResource, self).obj_create(bundle, **kwargs)
            
            # event=Event.objects.get(pk=bundle.)

        except DuplicateError:
          raise BadRequest('like already.')
            # usernamelist=[user.username for user in CustomUser.objects.all()]
            # if bundle.data['username'] in usernamelist:
            #     raise BadRequest('Username -'+bundle.data['username']+'- has been used.')
            # emaillist=[user.email for user in CustomUser.objects.all()]
            # if bundle.data['email'] in emaillist:
            #     raise BadRequest('Email -'+bundle.data['email']+'- has been used.')
        # event=Event.objects.get(pk=bundle.obj.fk_event_id)
        event.event_like=len(EventLike.objects.filter(fk_event__id=event.id))
        event.save()
        return bundle

class EventCommentResource(ModelResource):
    fk_comment_poster_user = fields.ForeignKey(UserResource, 'fk_comment_poster_user')

    class Meta:
        queryset = EventComment.objects.all()
        authentication = CustomAuthentication()
        authorization = EventRSVPCustomAuthorization()
        # ordering = ['event_date', 'event_time', 'event_create_time',
        #             'event_view_count', 'event_rsvp', 'event_like']
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
        #import pdb;pdb.set_trace()
        bundle.data['event_rsvp_count'] = Event.objects.get(id=bundle.obj.id).get_event_rsvp_count()
        bundle.data['event_like_count'] = Event.objects.get(id=bundle.obj.id).get_event_like_count()
        bundle.data['fk_event_poster_user_name'] = bundle.obj.fk_event_poster_user.username
        return bundle
