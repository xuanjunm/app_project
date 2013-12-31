import datetime
from django.utils import timezone
from django.views import generic
from events.models import *

from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.core.urlresolvers import reverse

# Handles view authorizations
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required

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

    def post(self, request, *args, **kwargs):
        self.object = None
        form_class = self.get_form_class()
        form = self.get_form(form_class)

        form.instance.fk_event_poster_user = request.user

        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def get_success_url(self):
        return reverse('events:events_list')

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(CreateEventView, self).dispatch(*args, **kwargs)

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

