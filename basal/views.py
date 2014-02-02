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

#    def get_context_data(self, **kwargs):
#        context = super(DashboardView, self).get_context_data(**kwargs)
#
#        try:
#            user_profile = UserProfile.objects.get(user=self.request.user.id)
#        except UserProfile.DoesNotExist:
#            user_profile = UserProfile(user=self.request.user)
#            user_profile.save()

#        context['user_profile'] = user_profile
#        return context

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

class AddressDetailView(generic.DetailView):
    template_name = 'basal/address_detail.html'
    model = Address

    def get_context_data(self, **kwargs):
        context = super(AddressDetailView, self).get_context_data(**kwargs)
        if self.request.GET.get('path_from'):
            context['path_from'] = self.request.GET.get('path_from')

        return context

class AddressCreateView(generic.CreateView):
    template_name = 'basal/address_create.html'
    model = Address

    def get_success_url(self):
        return self.request.POST.get('path_from')

    def get_context_data(self, **kwargs):
        context = super(AddressCreateView, self).get_context_data(**kwargs)
        if self.request.GET.get('path_from'):
            context['path_from'] = self.request.GET.get('path_from')

        return context

class AddressUpdateView(generic.UpdateView):
    template_name = 'basal/address_update.html'
    model = Address

    def get_success_url(self):
        return self.request.POST.get('path_from')

    def get_context_data(self, **kwargs):
        context = super(AddressUpdateView, self).get_context_data(**kwargs)
        if self.request.GET.get('path_from'):
            context['path_from'] = self.request.GET.get('path_from')

        return context
