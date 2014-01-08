from django.views import generic
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse

# import models
from django.contrib.auth.models import User
from .models import *

# Handles view authorizations
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required

# CreateUser
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, authenticate

class DashboardView(generic.TemplateView):
    template_name = 'basal/dashboard.html'

    def get_context_data(self, **kwargs):
        context = super(DashboardView, self).get_context_data(**kwargs)

        try:
            user = UserProfile.objects.get(user=self.request.user.id)
        except UserProfile.DoesNotExist:
            user = UserProfile(user=self.request.user)
            user.save()

        context['user_profile'] = user
        return context

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(DashboardView, self).dispatch(*args, **kwargs)

class UserCreate(generic.FormView):
    template_name = 'basal/user_create.html'
    form_class = UserCreationForm

    def form_valid(self, form):
        user = form.save()
        new_user_profile = UserProfile(user=user, user_gender='', 
                                       user_description='',
                                       user_nickname='')
        new_user_profile.save()

        new_user = authenticate(username=self.request.POST['username'],
                                password=self.request.POST['password1'])
        login(self.request, new_user)
        return HttpResponseRedirect(reverse('basal:dashboard'))
