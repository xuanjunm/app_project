from django.http import HttpResponse, HttpResponseRedirect
from django.views import generic
from django.shortcuts import get_object_or_404, render
from django.core.urlresolvers import reverse
#from django.template.loader import get_template

from events.models import *
from events.forms import *
from events.mixins import *

class EventsList(generic.ListView):
    template_name = 'events/events_list.html'
    context_object_name = "latest_events_list"
    def get_queryset(self):
        return Event.objects.order_by('-event_time')[:10]

class EventDetailsView(generic.DetailView):
    model = Event
    template_name = 'events/event_details.html'

class CreateEventView(MessageMixin, generic.CreateView):
    model = Event
#    form_class = EventForm
    template_name = 'events/create_event.html'
    success_message = 'Event has been created.'

    def get_success_url(self):
        return reverse('events:events_list')

class UpdateEventView(MessageMixin, generic.UpdateView):
    model = Event
#    form_class = EventForm
    template_name = 'events/update_event.html'
    success_message = 'Event has been updated.'

    def get_success_url(self):
        return reverse('events:event_details', args=(self.get_object().id,))

class DeleteEventView(MessageMixin, generic.DeleteView):
    model = Event
    template_name = 'events/delete_event.html'
    success_message = 'Event has been deleted.'

    def get_success_url(self):
        return reverse('events:events_list')

