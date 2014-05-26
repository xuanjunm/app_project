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

# use models from basal
from basal.models import UserImage

class EventListView(generic.TemplateView):
    template_name = 'events/event_list.html'

    def get_context_data(self, **kwargs):
        context = super(EventListView, self).get_context_data(**kwargs)

        today = timezone.now()
        temp = Event.objects.filter(event_date__gt=today)
#        import pdb;pdb.set_trace()
        temp = temp.order_by('-event_time')
        context['event_list'] = {}

        for i in range(0, temp.count()):
            event_owner = False
            event_rsvp = False
            if (temp[i].is_owner(self.request.user)):
                event_owner = True
            elif (temp[i].rsvp(self.request.user)):
                event_rsvp = True

            context['event_list'][temp[i].id] = temp[i]
            context['event_list'][temp[i].id].event_owner = event_owner 
            context['event_list'][temp[i].id].event_rsvp = event_rsvp
        return context

class EventDetailView(generic.DetailView):
    model = Event
    template_name = 'events/event_detail.html'

    def get_context_data(self, **kwargs):
        context = super(EventDetailView, self).get_context_data(**kwargs)
        c_event = Event.objects.get(pk=self.kwargs['pk'])
        context['comment_list'] = EventComment.objects.filter(fk_event=c_event.id).order_by('-comment_post_time')
                
        if (self.request.user) :
#            import pdb;pdb.set_trace()
            context['event_owner'] = c_event.is_owner(self.request.user)
            context['event_rsvp'] = c_event.rsvp(self.request.user)

        return context

class EventCreateView(generic.CreateView):
    template_name = 'events/event_create.html'
    form_class = EventCreateForm

    def post(self, request, *args, **kwargs):
        self.object = None
        form = self.get_form(self.form_class)

#        import pdb;pdb.set_trace()
        form.instance.fk_event_poster_user = request.user

        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def get_success_url(self):
        return reverse('events:event_list')

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(EventCreateView, self).dispatch(*args, **kwargs)

def authorized_to_update_event_decorator(fn):
    # a decorator to check login_user is the owner of an event
    def decorator(request, *args, **kwargs):
        if Event.objects.get(pk=kwargs['pk']).is_owner(request.user):
            return fn(request, *args, **kwargs)
        else:
            return HttpResponseRedirect(reverse('basal:user_login'))
    return decorator

class EventUpdateView(generic.UpdateView):
    model = Event
    form_class = EventUpdateForm
    template_name = 'events/event_update.html'

    def get_success_url(self):
        return reverse('events:event_detail', args=(self.kwargs['pk'],))

    @method_decorator(authorized_to_update_event_decorator)
    def dispatch(self, *args, **kwargs):
        return super(EventUpdateView, self).dispatch(*args, **kwargs)

class EventDeleteView(generic.DeleteView):
    model = Event
    template_name = 'events/event_delete.html'

    def get_success_url(self):
        return reverse('events:event_list')

    @method_decorator(authorized_to_update_event_decorator)
    def dispatch(self, *args, **kwargs):
        return super(EventDeleteView, self).dispatch(*args, **kwargs)

@login_required
def event_rsvp(request, pk):
#    import pdb;pdb.set_trace()
    c_event = Event.objects.get(pk=pk)
    new_rsvp = EventRSVP(fk_user=request.user, fk_event=c_event)
    new_rsvp.save()
    return HttpResponseRedirect(reverse('events:event_detail', args=(pk,)) + '#rsvps')

@login_required
def event_rsvp_remove(request, pk):
    c_event = Event.objects.get(pk=pk)
    c_rsvp = EventRSVP.objects.filter(
                fk_user=request.user).get(fk_event=c_event)
    c_rsvp.delete()
    return HttpResponseRedirect(reverse('events:event_detail', args=(pk,)) + '#rsvps')

@login_required
def event_comment_create(request, pk):
#    import pdb;pdb.set_trace()
    temp = request.POST.get('comment')
    if temp != '':
        c_event = Event.objects.get(pk=pk)
        new_comment = EventComment(fk_comment_poster_user=request.user, comment_detail=temp, fk_event=c_event)
        new_comment.save()
    return HttpResponseRedirect(reverse('events:event_detail', args=(pk,)) + '#comments')
