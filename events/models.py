from django.db import models
from basal.models import *
from django.contrib.auth.models import User

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
    event_type = models.CharField(max_length=10,
                            choices=EVENT_TYPE_CHOICES)
    event_status = models.CharField(max_length=10,
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
    event_recent_update = models.DateTimeField(auto_now_add=True)
    fk_event_poster_user = models.ForeignKey(User, 
                                             verbose_name='Event Poster')
    fk_address = models.ForeignKey(Address,
                                   verbose_name='Event Location',
                                   unique=False)

    def is_posted_by(self, user):
        return self.fk_event_poster_user==user

    def __unicode__(self):
        return self.event_title

class EventSubscription(models.Model):
    fk_subscriber_user = models.ForeignKey(User)
    fk_subscribed_event = models.ForeignKey(Event)

    def __unicode__(self):
        return self.fk_subscriber_user

class EventComment(models.Model):
    comment_detail = models.TextField()
    comment_post_time = models.DateTimeField(auto_now_add=True)
    fk_event = models.ForeignKey(Event)
    fk_comment_poster_user = models.ForeignKey(User)

    def __unicode__(self):
        return self.fk_comment_poster_event

class Tag(models.Model):
    tag_name = models.CharField(max_length=255)

    def __unicode__(self):
        return self.tag_name

class TagEventAttribute(models.Model):
    fk_tag = models.ForeignKey(Tag)
    fk_event = models.ForeignKey(Event)

    def __unicode__(self):
        return self.fk_tag
