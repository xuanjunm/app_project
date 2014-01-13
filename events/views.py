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
#    form_class_2 = AddressForm

#    def form_invalid(self, form, form_2):
#        """
#        will return the 2 forms with user inputs
#        """
#        return self.render_to_response(self.get_context_data(form=form,
#                                                             form_2=form_2))

    def post(self, request, *args, **kwargs):
        self.object = None
        form = self.get_form(self.form_class)
#        form_2 = self.get_form(self.form_class_2)

        # let fk_event_poster_user = current login user
        form.instance.fk_event_poster_user = request.user

        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

        # if AddressForm is valid, check EventCreateForm
#        if form_2.is_valid():
#            form_2_object = form_2.save()
#            form.instance.fk_address = form_2_object
        #    import pdb;pdb.set_trace()

#            if form.is_valid():
#                return self.form_valid(form)
#            else:
#                form_2_object.delete()
#                return self.form_invalid(form, form_2)
#        else:
#            return self.form_invalid(form, form_2)

#        import pdb;pdb.set_trace()
#    def get_context_data(self, **kwargs):
#        context = super(EventCreateView, self).get_context_data(**kwargs)

#        if 'form_2' not in context: 
#            context['form_2'] = self.form_class_2

#        return context

    def get_success_url(self):
        return reverse('events:event_list')

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
#    form_class_2 = AddressForm
    template_name = 'events/event_update.html'

#    def post(self, request, *args, **kwargs):
#        self.object = self.get_object()
#        if 'event_form' in request.POST:
#            form_class = self.get_form_class()
#            form_name = 'form'
#        else:
#            form_class = self.form_class_2
#            form_name = 'form_2'
#
#        form = self.get_form(form_class)
#
#        if form.is_valid():
#            return self.form_valid(form)
#        else:
#            return self.form_invalid(**{form_name: form})

    def get_success_url(self):
        return reverse('events:event_detail', args=(self.get_object().id,))

#    def get_context_data(self, **kwargs):
#        context = super(EventUpdateView, self).get_context_data(**kwargs)
#
#        # include Address of the Event in view
#        context['form_2'] = self.form_class_2(
#                initial=model_to_dict(self.get_object().fk_address))
#        #        import pdb;pdb.set_trace()
#        return context

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

class AddressCreateView(generic.CreateView):
    template_name = 'events/address_create.html'
    model = Address

class AddressUpdateView(generic.UpdateView):
    template_name = 'events/address_update.html'
    model = Address


