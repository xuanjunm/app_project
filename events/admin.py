from django.contrib import admin
from events.models import *

class EventAdmin(admin.ModelAdmin):
#    fields = ['event_name', 'date', 'organizer', 'no_of_rsvp']
    list_display = ['event_name', 'event_type', 'event_location',
                    'event_time', 'event_organizer_id', 'event_status']
    list_filter = ['event_time']
    date_hierarchy = 'event_time'

class EventSubscriptionAdmin(admin.ModelAdmin):
    list_display = ['subscriber_account_id', 'event_id']

class EventMessageAdmin(admin.ModelAdmin):
    list_display = ['poster_account_id', 'event_id']

admin.site.register(Event, EventAdmin)
admin.site.register(EventSubscription, EventSubscriptionAdmin)
admin.site.register(EventMessage, EventMessageAdmin)
