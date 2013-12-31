import datetime
from django.utils import timezone
from django.views import generic
from events.models import *

from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.core.urlresolvers import reverse
#from events.mixins import *

# for CreateEventView
from .forms import *

class EventsList(generic.ListView):
    template_name = 'events/events_list.html'
    context_object_name = "events_list"

    def get_queryset(self):
        today = timezone.now()
        temp = Event.objects.filter(event_time__gt=today)
#        import pdb;pdb.set_trace()
        return temp.order_by('-event_time')

class EventDetailsView(generic.DetailView):
    model = Event
    template_name = 'events/event_details.html'

class CreateEventView(generic.CreateView):
    model = Event
    form_class = EventCreateForm
    template_name = 'events/create_event.html'

    def get_initial(self):
        # get the initial dict from the superclass method
        initial = super(CreateEventView, self).get_initial()
        # copy the dict so we don't accidentally change a mutable dict
        initial = initial.copy()
        initial['fk_event_poster_user'] = self.request.user

        return initial

    def get_success_url(self):
        return reverse('events:events_list')

class UpdateEventView(generic.UpdateView):
    model = Event
#    form_class = EventForm
    template_name = 'events/update_event.html'

    def get_success_url(self):
        return reverse('events:event_details', args=(self.get_object().id,))

class DeleteEventView(generic.DeleteView):
    model = Event
    template_name = 'events/delete_event.html'

    def get_success_url(self):
        return reverse('events:events_list')

