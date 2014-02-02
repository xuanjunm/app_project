from django import forms 
from .models import *

class EventCreateForm(forms.ModelForm):
    class Meta:
        model = Event
        exclude = ['fk_event_poster_user', 'event_like', 'event_rsvp', 
                   'event_view_count', 'event_status']

#class AddressForm(forms.ModelForm):
#    class Meta:
#        model = Address
#        exclude = ['fk_event']

class EventUpdateForm(forms.ModelForm):
    class Meta:
        model = Event
        exclude = ['fk_event_poster_user', 'event_like', 'event_rsvp', 
                   'event_view_count']
