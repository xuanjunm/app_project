from django.views import generic
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.shortcuts import get_object_or_404

# import models
from .models import *

# Handles view authorizations
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required

# User
from django.contrib.auth import login, authenticate

# UserUpdate
from .forms import *

class DashboardView(generic.TemplateView):
    template_name = 'basal/dashboard.html'

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(DashboardView, self).dispatch(*args, **kwargs)

class UserCreateView(generic.CreateView):
    template_name = 'basal/user_create.html'
    form_class = CustomUserCreationForm

    def form_valid(self, form):
        user = form.save()

        new_user = authenticate(username=self.request.POST['username'],
                                 password=self.request.POST['password1'])
        login(self.request, new_user)
        return HttpResponseRedirect(reverse('basal:dashboard'))

class UserUpdateView(generic.UpdateView):
    template_name = 'basal/user_update.html'
    form_class = UserUpdateForm

    def get_object(self, queryset=None):
        obj = get_object_or_404(CustomUser, pk=self.request.user.pk)
        return obj

    def get_success_url(self):
        return reverse('basal:dashboard')

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(UserUpdateView, self).dispatch(*args, **kwargs)

def authorized_to_update_address_decorator(fn):
    # a decorator to check login_user is the owner of an event
    def decorator(request, *args, **kwargs):
        if Event.objects.get(pk=kwargs['pk']).is_posted_by(request.user):
            return fn(request, *args, **kwargs)
        else:
            return HttpResponseRedirect(reverse('basal:user_login'))
    return decorator

class AddressListView(generic.ListView):
    template_name = 'basal/address_list.html'
    model = Address

    def get_context_data(self, **kwargs):
        context = super(AddressListView, self).get_context_data(**kwargs)
        #if self.request.GET.get('next'):
        #context['next'] = self.request.GET.get('next')
        context['next'] = self.request.get_full_path()
        return context

class AddressDetailView(generic.DetailView):
    template_name = 'basal/address_detail.html'
    model = Address

    def get_context_data(self, **kwargs):
        context = super(AddressDetailView, self).get_context_data(**kwargs)
        if self.request.GET.get('next'):
            context['next'] = self.request.GET.get('next')
        return context

class AddressCreateView(generic.CreateView):
    template_name = 'basal/address_create.html'
    model = Address

    def get_success_url(self):
        return self.request.POST.get('next')

    def get_context_data(self, **kwargs):
        context = super(AddressCreateView, self).get_context_data(**kwargs)
        if self.request.GET.get('next'):
            context['next'] = self.request.GET.get('next')
        return context

class AddressUpdateView(generic.UpdateView):
    template_name = 'basal/address_update.html'
    model = Address

    def get_success_url(self):
        return self.request.POST.get('next')

    def get_context_data(self, **kwargs):
        context = super(AddressUpdateView, self).get_context_data(**kwargs)
        if self.request.GET.get('next'):
            context['next'] = self.request.GET.get('next')
        return context

class AddressDeleteView(generic.DeleteView):
    template_name = 'basal/address_delete.html'
    model = Address

    def get_success_url(self):
        return self.request.POST.get('next')

    def get_context_data(self, **kwargs):
        context = super(AddressDeleteView, self).get_context_data(**kwargs)
        if self.request.GET.get('next'):
            context['next'] = self.request.GET.get('next')
        return context
