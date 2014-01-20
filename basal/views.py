from django.views import generic
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.shortcuts import get_object_or_404

# import models
from django.contrib.auth.models import User
from .models import *

# Handles view authorizations
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required

# CreateUser
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, authenticate

# UserUpdate
from .forms import *

class DashboardView(generic.TemplateView):
    template_name = 'basal/dashboard.html'

    def get_context_data(self, **kwargs):
        context = super(DashboardView, self).get_context_data(**kwargs)

        try:
            user_profile = UserProfile.objects.get(user=self.request.user.id)
        except UserProfile.DoesNotExist:
            user_profile = UserProfile(user=self.request.user)
            user_profile.save()

        context['user_profile'] = user_profile
        return context

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(DashboardView, self).dispatch(*args, **kwargs)

class UserCreateView(generic.FormView):
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

class UserUpdateView(generic.UpdateView):
    template_name = 'basal/user_update.html'
    form_class = UserProfileUpdateForm
#    form_class_2 = UserProfileUpdateForm

#    def post(self, request, *args, **kwargs):
#        update_user = User.objects.get(id=request.user.id)
#        form = self.get_form(self.form_class)
#        form = self.form_class({'instance':update_user,
#                                'data':request.POST})
#        form_2 = self.get_form(self.form_class_2)

#        import pdb;pdb.set_trace()

#        if form.is_valid():# and form_2.is_valid():
    #        form_data = form.save(commit=False)
    #        form_data.save()
#            form.save()
#            return HttpResponseRedirect(self.get_success_url())
#        else:
#            return self.render_to_response(
#                    self.get_context_data(form=form, form_2=form_2))
        

    def get_object(self, queryset=None):
        obj = get_object_or_404(UserProfile, user=self.request.user)
        return obj

    def get_success_url(self):
        return reverse('basal:dashboard')

#    def get_context_data(self, **kwargs):
#        context = super(UserUpdateView, self).get_context_data(**kwargs)

#        if 'form_2' not in context:
#            try:
#                user_profile = UserProfile.objects.get(user=self.request.user)
#            except UserProfile.DoesNotExist:
#                user_profile = UserProfile(user=self.request.user)
#                user_profile.save()
    
#            context['form_2'] = self.form_class_2(instance=user_profile)
#        return context

