from django.views import generic
from django.contrib.auth.models import User
from .models import *
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required

class DashboardView(generic.TemplateView):
    template_name = 'patio/dashboard.html'

    def get_context_data(self, **kwargs):
        context = super(DashboardView, self).get_context_data(**kwargs)
        user = UserProfile.objects.get(user=self.request.user.id)

        context['user_profile'] = user
        return context

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(DashboardView, self).dispatch(*args, **kwargs)
