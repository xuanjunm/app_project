from django.contrib import admin
from .models import *

class AddressInline(admin.StackedInline):
    model = Address
    can_delete = False

class EventAdmin(admin.ModelAdmin):
    list_display = ['event_title', 'event_type', 'event_time', 
                    'fk_event_poster_user', 'event_status']
    list_filter = ['event_time']
    date_hierarchy = 'event_time'
    inlines = [AddressInline]

class EventSubscriptionAdmin(admin.ModelAdmin):
    list_display = ['fk_subscriber_user', 'fk_subscribed_event']

class EventCommentAdmin(admin.ModelAdmin):
    list_display = ['fk_comment_poster_user', 'fk_event']

admin.site.register(Event, EventAdmin)
admin.site.register(EventSubscription, EventSubscriptionAdmin)
admin.site.register(EventComment, EventCommentAdmin)
