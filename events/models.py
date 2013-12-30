from django.db import models
from patio.models import Account

class Event(models.Model):
    EVENT_TYPE_CHOICES = (
        ('public', 'public'),
        ('private', 'private'),
    )
    
    EVENT_STATUS_CHOICES = (
        ('active', 'active'),
        ('inactive', 'inactive'),
    )
    event_name = models.CharField(max_length=255)
    event_type = models.CharField(max_length=10,
                                  choices=EVENT_TYPE_CHOICES)
    event_location = models.CharField(max_length=255)
    event_status = models.CharField(max_length=10,
                                    choices=EVENT_STATUS_CHOICES,
                                    default='active')
    event_time = models.DateTimeField('event time')
    event_create_time = models.DateTimeField(auto_now_add=True)
    event_details = models.TextField(blank=True)
    event_organizer_id = models.ForeignKey(Account)

    def __unicode__(self):
        return self.event_name

class EventSubscription(models.Model):
    subscriber_account_id = models.ForeignKey(Account)
    event_id = models.ForeignKey(Event)

    def __unicode__(self):
        return self.subscriber_account_id.account_name

class EventMessage(models.Model):
    event_message_detail = models.CharField(max_length=255)
    poster_account_id = models.ForeignKey(Account)
    event_id = models.ForeignKey(Event)

    def __unicode__(self):
        return self.poster_account_id.account_name
