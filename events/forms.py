from django.forms import ModelForm
from .models import *

class EventCreateForm(ModelForm):
    class Meta:
        model = Event
        exclude = ['fk_event_poster_user', 'event_like', 'event_rsvp', 
                   'event_view_count', 'event_status']
