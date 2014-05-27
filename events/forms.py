from django import forms 
from .models import *
from basal.forms import metaForm

class EventCreateForm(metaForm):
    EVENT_TYPE_CHOICES=[('public','public'),('private','private')]
    event_type = forms.ChoiceField(choices=EVENT_TYPE_CHOICES, widget=forms.RadioSelect, initial='public')

    class Meta:
        model = Event
        exclude = ['fk_event_poster_user', 'event_like', 'event_rsvp', 
                   'event_view_count', 'event_status']

    def __init__(self, *args, **kwargs):
        super(EventCreateForm, self).__init__(*args, **kwargs)
        self.fields['event_type'].widget.attrs['class'] = ''

#class AddressForm(forms.ModelForm):
#    class Meta:
#        model = Address
#        exclude = ['fk_event']

class EventUpdateForm(metaForm):
    EVENT_TYPE_CHOICES=[('public','public'),('private','private')]
    event_type = forms.ChoiceField(choices=EVENT_TYPE_CHOICES, widget=forms.RadioSelect, initial='public')

    EVENT_STATUS_CHOICES=[('active','active'),('inactive','inactive')]
    event_status = forms.ChoiceField(choices=EVENT_STATUS_CHOICES, widget=forms.RadioSelect, initial='active')

    class Meta:
        model = Event
        exclude = ['fk_event_poster_user', 'event_like', 'event_rsvp', 
                   'event_view_count']

    def __init__(self, *args, **kwargs):
        '''
        to remove the selected box around options
        '''
        super(EventUpdateForm, self).__init__(*args, **kwargs)
        self.fields['event_type'].widget.attrs['class'] = ''
        self.fields['event_status'].widget.attrs['class'] = ''

class EventCommentCreateForm(forms.ModelForm):
	class Meta:
		model=EventComment
		exclude=['fk_event', 'fk_comment_poster_user','comment_post_time']

class EventImageForm(forms.ModelForm):
    class Meta:
        model = EventImage
        exclude = ['fk_event']
