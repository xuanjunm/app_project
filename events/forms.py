from django import forms
from events.models import *

EVENT_TYPE_CHOICES = (
    ('public', 'public'),
    ('private', 'private'),
)

class EventForm(forms.ModelForm):
    class Meta:
        model = Event

    event_name = forms.CharField(label='Event name *')
    event_type = forms.CharField(label='Event type *',
                            widget=forms.Select(choices=EVENT_TYPE_CHOICES))
    event_location = forms.CharField(label='Event location *')
    event_time = forms.DateTimeField(label='Event time *')
    event_organizer_id = forms.ModelChoiceField(queryset=Account.objects.all(),
                            label='Event organizer *')
