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
    event_rsvp = models.PositiveSmallIntegerField(default=0)
    event_like = models.PositiveSmallIntegerField(default=0)
    event_recent_update = models.DateTimeField(auto_now=True)
    fk_event_image = models.TextField('event_image')
    fk_event_poster_user = models.ForeignKey(CustomUser, 
                                             verbose_name='Event Poster')
    fk_address = models.ForeignKey(Address,
                                   verbose_name='Event Location',
                                   unique=False)

    def is_owner(self, user):
        return self.fk_event_poster_user == user
    
    def rsvp(self, user):
        try:
            self.eventrsvp_set.get(fk_user=user.id)
        except EventRSVP.DoesNotExist:
            return False
        else:
            return True

    def __unicode__(self):
        return self.event_title

class EventRSVP(models.Model):
    fk_user = models.ForeignKey(CustomUser)
    fk_event = models.ForeignKey(Event)

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
# if similar EventLike object exists, then it wouldn't be saved
#        else:
#            raise OperationalError

class EventComment(models.Model):
    comment_detail = models.TextField()
    comment_post_time = models.DateTimeField(auto_now_add=True)
    fk_event = models.ForeignKey(Event)
    fk_comment_poster_user = models.ForeignKey(CustomUser)

    def __unicode__(self):
        return self.fk_comment_poster_event

class Tag(models.Model):
    tag_name = models.CharField(unique=True, max_length=255)

    def __unicode__(self):
        return self.tag_name

class TagEventAttribute(models.Model):
    fk_tag = models.ForeignKey(Tag)
    fk_event = models.ForeignKey(Event)

    def __unicode__(self):
        return self.fk_tag
