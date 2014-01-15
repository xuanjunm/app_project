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
from django.forms.models import model_to_dict

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

class EventDetailView(generic.DetailView):
    model = Event
    template_name = 'events/event_detail.html'

class EventCreateView(generic.CreateView):
    template_name = 'events/event_create.html'
    form_class = EventCreateForm

    def post(self, request, *args, **kwargs):
        self.object = None
        form = self.get_form(self.form_class)

        # let fk_event_poster_user = current login user
        form.instance.fk_event_poster_user = request.user

        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def get_success_url(self):
        return reverse('events:event_list')

    def get_context_data(self, **kwargs):
        context = super(EventCreateView, self).get_context_data(**kwargs)
        context['path_current'] = self.request.get_full_path()
#        import pdb;pdb.set_trace()
        return context


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
        return reverse('events:event_detail', args=(self.get_object().id,))

    def get_context_data(self, **kwargs):
        context = super(EventUpdateView, self).get_context_data(**kwargs)
        context['path_current'] = self.request.get_full_path()
#        import pdb;pdb.set_trace()
        return context

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

class AddressDetailView(generic.DetailView):
    template_name = 'events/address_detail.html'
    model = Address

    def get_context_data(self, **kwargs):
        context = super(AddressDetailView, self).get_context_data(**kwargs)
        if self.request.GET.get('path_from'):
            context['path_from'] = self.request.GET.get('path_from')

        return context

class AddressCreateView(generic.CreateView):
    template_name = 'events/address_create.html'
    model = Address

    def get_success_url(self):
        return self.request.POST.get('path_from')

    def get_context_data(self, **kwargs):
        context = super(AddressCreateView, self).get_context_data(**kwargs)
        if self.request.GET.get('path_from'):
            context['path_from'] = self.request.GET.get('path_from')

        return context

class AddressUpdateView(generic.UpdateView):
    template_name = 'events/address_update.html'
    model = Address

    def get_success_url(self):
        return self.request.POST.get('path_from')

    def get_context_data(self, **kwargs):
        context = super(AddressUpdateView, self).get_context_data(**kwargs)
        if self.request.GET.get('path_from'):
            context['path_from'] = self.request.GET.get('path_from')

        return context
