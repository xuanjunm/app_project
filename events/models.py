from django.db import models
from django.db import OperationalError
from basal.models import *

class Event(models.Model):
    EVENT_TYPE_CHOICES = (
        ('public', 'public'),
        ('private', 'private'),
    )
    
    EVENT_STATUS_CHOICES = (
        ('active', 'active'),
        ('inactive', 'inactive'),
    )

    event_title = models.CharField(max_length=255)
    event_type = models.CharField(max_length=255,
                                 choices=EVENT_TYPE_CHOICES,
                                 default='public')
    event_status = models.CharField(max_length=255,
                                    choices=EVENT_STATUS_CHOICES,
                                    default='active')
    event_date = models.DateField('event date')
    event_time = models.TimeField('event time')
    event_create_time = models.DateTimeField(auto_now_add=True)
    event_detail = models.TextField(blank=True)
    event_view_count = models.PositiveSmallIntegerField(default=0)
    event_capacity = models.PositiveSmallIntegerField(blank=True, null=True)
    event_recent_update = models.DateTimeField(auto_now=True)
    fk_event_poster_user = models.ForeignKey(CustomUser, 
                                             verbose_name='Event Poster')

# event address
    address_detail = models.CharField(max_length=255)
    address_city = models.CharField(blank=True, max_length=255)
    address_region = models.CharField(blank=True, max_length=255)
    address_country = models.CharField(blank=True, 
                                       max_length=255, 
                                       default='Canada')
    address_postal_code = models.CharField(blank=True, max_length=255)

    def is_owner(self, user):
        return self.fk_event_poster_user == user
    
    def rsvp(self, user):
        try:
            self.eventrsvp_set.get(fk_user=user.id)
        except EventRSVP.DoesNotExist:
            return False
        else:
            return True

    def get_event_rsvp_count(self):
#        import pdb;pdb.set_trace()
        return EventRSVP.objects.filter(fk_event=self).count() 

    def get_event_like_count(self):
#        import pdb;pdb.set_trace()
        return EventLike.objects.filter(fk_event=self).count() 

    def __unicode__(self):
        return self.event_title

class EventRSVP(models.Model):
    fk_user = models.ForeignKey(CustomUser)
    fk_event = models.ForeignKey(Event)

    def __unicode__(self):
        return self.fk_user.username+" rsvps "+self.fk_event.event_title

class EventLike(models.Model):
    fk_user = models.ForeignKey(CustomUser)
    fk_event = models.ForeignKey(Event)

    def exists(self):
        try:
            temp = EventLike.objects.filter(fk_user=self.fk_user.id)
            temp.get(fk_event=self.fk_event.id)
        except EventLike.DoesNotExist, EventLike.MultipleObjectsReturned:
            return False
        else:
            return True

    def save(self):
        if not self.exists():
            super(EventLike, self).save()

    def __unicode__(self):
        return self.fk_user.username+" likes "+self.fk_event.event_title
# if similar EventLike object exists, then it wouldn't be saved
#        else:
#            raise OperationalError

class EventComment(models.Model):
    comment_detail = models.TextField()
    comment_post_time = models.DateTimeField(auto_now_add=True)
    fk_event = models.ForeignKey(Event, related_name='event_comment')
    fk_comment_poster_user = models.ForeignKey(CustomUser)

    def __unicode__(self):
        return u'%s' % self.fk_event

class Tag(models.Model):
    tag_name = models.CharField(unique=True, max_length=255)

    def __unicode__(self):
        return self.tag_name

class TagEventAttribute(models.Model):
    fk_tag = models.ForeignKey(Tag)
    fk_event = models.ForeignKey(Event)

    def __unicode__(self):
        return self.fk_tag

class EventImage(models.Model):
    path = models.ImageField(upload_to='event_image', 
                             help_text='help text')
    fk_event = models.ForeignKey(Event, related_name='event_image')

    def __unicode__(self):
        return u'%s' % self.path
