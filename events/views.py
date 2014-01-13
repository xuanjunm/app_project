import datetime
from django.utils import timezone
from django.views import generic
from events.models import *

from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.core.urlresolvers import reverse

# Handles view authorizations
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required, user_passes_test

# for EventCreateView
from .forms import *

class EventList(generic.ListView):
    template_name = 'events/event_list.html'
    context_object_name = "event_list"

    def get_queryset(self):
        today = timezone.now()
        temp = Event.objects.filter(event_time__gt=today)
#        import pdb;pdb.set_trace()
        return temp.order_by('-event_time')

class EventDetailsView(generic.DetailView):
    model = Event
    template_name = 'events/event_details.html'

class EventCreateView(generic.CreateView):
    template_name = 'events/event_create.html'
    form_class = EventCreateForm
    form_class_2 = AddressForm

    def form_invalid(self, form, form_2):
        """
        will return the 2 forms with user inputs
        """
        return self.render_to_response(self.get_context_data(form=form,
                                                             form_2=form_2))

    def post(self, request, *args, **kwargs):
        self.object = None
        form = self.get_form(self.form_class)
        form_2 = self.get_form(self.form_class_2)

        # let fk_event_poster_user = current login user
        form.instance.fk_event_poster_user = request.user

        # if AddressForm is valid, check EventCreateForm
        if form_2.is_valid():
            form_2_object = form_2.save()
            form.instance.fk_address = form_2_object
#            import pdb;pdb.set_trace()

            if form.is_valid():
                return self.form_valid(form)
            else:
                form_2_object.delete()
                return self.form_invalid(form, form_2)
        else:
            return self.form_invalid(form, form_2)

#        import pdb;pdb.set_trace()
    def get_context_data(self, **kwargs):
        context = super(EventCreateView, self).get_context_data(**kwargs)

        if 'form_2' not in context: 
            context['form_2'] = self.form_class_2

        return context

    def get_success_url(self):
        return reverse('events:events_list')

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(EventCreateView, self).dispatch(*args, **kwargs)

def authorized_to_update_decorator(fn):
    # a decorator to check login_user is the owner of an event
    def decorator(request, *args, **kwargs):
        if Event.objects.get(pk=kwargs['pk']).is_posted_by(request.user):
            return fn(request, *args, **kwargs)
        else:
            return HttpResponseRedirect(reverse('basal:user_login'))
    return decorator

class EventUpdateView(generic.UpdateView):
    model = Event
    form_class = EventUpdateForm
    template_name = 'events/event_update.html'

    def get_success_url(self):
        return reverse('events:event_details', args=(self.get_object().id,))

    @method_decorator(authorized_to_update_decorator)
    def dispatch(self, *args, **kwargs):
        return super(EventUpdateView, self).dispatch(*args, **kwargs)

class EventDeleteView(generic.DeleteView):
    model = Event
    template_name = 'events/event_delete.html'

    def get_success_url(self):
        return reverse('events:event_list')

    @method_decorator(authorized_to_update_decorator)
    def dispatch(self, *args, **kwargs):
        return super(EventDeleteView, self).dispatch(*args, **kwargs)
