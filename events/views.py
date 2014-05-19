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

class EventListView(generic.ListView):
    template_name = 'events/event_list.html'
    context_object_name = "event_list"

    def get_queryset(self):
        today = timezone.now()
        temp = Event.objects.filter(event_date__gt=today)
#        import pdb;pdb.set_trace()
        return temp.order_by('-event_time')

#    def get_context_data(self, **kwargs):
#        context = super(EventListView, self).get_context_data(**kwargs)
#
#        return context

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

        if self.request.GET.get('back'):
            context['back'] = self.request.GET.get('back')
        context['current_path'] = self.request.get_full_path()
        return context

class EventCreateView(generic.CreateView):
    template_name = 'events/event_create.html'
    form_class = EventCreateForm

    def post(self, request, *args, **kwargs):
        self.object = None
        form = self.get_form(self.form_class)

        form.instance.fk_event_poster_user = request.user

        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def get_success_url(self):
        return reverse('events:event_list')

    def get_form(self, form_class):
        form = super(EventCreateView, self).get_form(form_class)
        c_address = Address.objects.filter(fk_user=self.request.user)
        form.fields['fk_address'].queryset = c_address 
        return form

    def get_context_data(self, **kwargs):
        context = super(EventCreateView, self).get_context_data(**kwargs)
        context['current_path'] = self.request.get_full_path()
#        import pdb;pdb.set_trace()
        return context

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
        return self.request.POST.get('back')

    def get_form(self, form_class):
        form = super(EventUpdateView, self).get_form(form_class)
        c_address = Address.objects.filter(fk_user=self.request.user)
        form.fields['fk_address'].queryset = c_address 
        return form

    def get_context_data(self, **kwargs):
        context = super(EventUpdateView, self).get_context_data(**kwargs)
        if self.request.GET.get('back'):
            context['back'] = self.request.GET.get('back')
        context['current_path'] = self.request.get_full_path() 
#        import pdb;pdb.set_trace()
        return context

    @method_decorator(authorized_to_update_event_decorator)
    def dispatch(self, *args, **kwargs):
        return super(EventUpdateView, self).dispatch(*args, **kwargs)

class EventDeleteView(generic.DeleteView):
    model = Event
    template_name = 'events/event_delete.html'

    def get_success_url(self):
        return self.request.POST.get('back')

    @method_decorator(authorized_to_update_event_decorator)
    def dispatch(self, *args, **kwargs):
        return super(EventDeleteView, self).dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(EventDeleteView, self).get_context_data(**kwargs)
        if self.request.GET.get('back'):
            context['back'] = self.request.GET.get('back')
#        import pdb;pdb.set_trace()
        return context


@login_required
def event_rsvp(request, pk):
#    import pdb;pdb.set_trace()
    c_event = Event.objects.get(pk=pk)
    new_rsvp = EventRSVP(fk_user=request.user, fk_event=c_event)
    new_rsvp.save()
    if request.GET.get('back'):
        return HttpResponseRedirect(request.GET.get('back'))
    else:
        return HttpResponseRedirect(reverse('events:event_detail', args=(pk,)))

@login_required
def event_rsvp_remove(request, pk):
    c_event = Event.objects.get(pk=pk)
    c_rsvp = EventRSVP.objects.filter(
                fk_user=request.user).get(fk_event=c_event)
    c_rsvp.delete()
    if request.GET.get('back'):
        return HttpResponseRedirect(request.GET.get('back'))
    else:
        return HttpResponseRedirect(reverse('events:event_detail', args=(pk,)))

class EventCommentCreateView(generic.CreateView):
    model = EventComment
    form_class=EventCommentCreateForm
    template_name = 'events/event_comment_create.html'

    def post(self, request, *args, **kwargs):
        self.object = None
        form = self.get_form(self.form_class)

        form.instance.fk_comment_poster_user = request.user
        form.instance.fk_event = Event.objects.get(pk=self.kwargs['pk'])

        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def get_success_url(self):
            return self.request.POST.get('back')

    def get_context_data(self, **kwargs):
        context = super(EventCommentCreateView, self).get_context_data(**kwargs)
        context['pk'] = self.kwargs['pk']
        if self.request.GET.get('back'):
            context['back'] = self.request.GET.get('back')

#        import pdb;pdb.set_trace()
        return context

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(EventCommentCreateView, self).dispatch(*args, **kwargs)
