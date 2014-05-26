from django.views import generic
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.shortcuts import get_object_or_404

# import models
from .models import *
from events.models import *

# Handles view authorizations
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required

# User
from django.contrib.auth import login, authenticate

# UserUpdate
from .forms import *

# work around for image upload
from django.views.decorators.csrf import csrf_exempt
from tastypie.models import ApiKey

class DashboardView(generic.TemplateView):
    template_name = 'basal/dashboard.html'

    def get_context_data(self, **kwargs):
        context = super(DashboardView, self).get_context_data(**kwargs)

        temp = Address.objects.filter(fk_user=self.request.user)
#        import pdb;pdb.set_trace()
        context['address_list'] = temp

        temp = Event.objects.filter(fk_event_poster_user=self.request.user)
        context['event_list'] = temp

        temp = EventRSVP.objects.filter(fk_user=self.request.user)
        context['rsvp_list'] = temp

        temp = UserTagAttribute.objects.filter(fk_user=self.request.user)
        context['tag_list'] = temp

        context['current_path'] = self.request.get_full_path()

        return context

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
    # a decorator to check login_user is the owner of an address
    def decorator(request, *args, **kwargs):
        if Address.objects.get(pk=kwargs['pk']).is_owner(request.user):
            return fn(request, *args, **kwargs)
        else:
            return HttpResponseRedirect(reverse('basal:user_login'))
    return decorator

class AddressCreateView(generic.CreateView):
    template_name = 'basal/address_create.html'
    model = Address
    form_class = AddressForm

    def post(self, request, *args, **kwargs):
        self.object = None
        form = self.get_form(self.form_class)

        # let fk_user = current login user
        form.instance.fk_user = request.user

        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def get_success_url(self):
        return reverse('basal:dashboard') + '#addresses'
    
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(AddressCreateView, self).dispatch(*args, **kwargs)


class AddressUpdateView(generic.UpdateView):
    template_name = 'basal/address_update.html'
    model = Address
    form_class = AddressForm

    def get_success_url(self):
        return reverse('basal:dashboard') + '#addresses' 

    @method_decorator(authorized_to_update_address_decorator)
    def dispatch(self, *args, **kwargs):
        return super(AddressUpdateView, self).dispatch(*args, **kwargs)

class AddressDeleteView(generic.DeleteView):
    template_name = 'basal/address_delete.html'
    model = Address

    def get_success_url(self):
        return reverse('basal:dashboard') + '#addresses'

    @method_decorator(authorized_to_update_address_decorator)
    def dispatch(self, *args, **kwargs):
        return super(AddressDeleteView, self).dispatch(*args, **kwargs)

def authorized_to_update_user_image_decorator(fn):
    # a decorator to check login_user is the owner of an user_image
    def decorator(request, *args, **kwargs):
        if UserImage.objects.get(pk=kwargs['pk']).is_owner(request.user):
            return fn(request, *args, **kwargs)
        else:
            return HttpResponseRedirect(reverse('basal:user_login'))
    return decorator

class UserDetailView(generic.TemplateView):
    template_name = 'basal/user_detail.html'

    def get_context_data(self, **kwargs):
        context = super(UserDetailView, self).get_context_data(**kwargs)

        t_user = CustomUser.objects.get(id=kwargs['pk'])
        context['t_user'] = t_user

        temp = EventRSVP.objects.filter(fk_user=t_user)
        context['rsvp_list'] = {}

        for i in range(0, temp.count()):
            event_owner = False
            event_rsvp = False
            if (temp[i].fk_event.is_owner(self.request.user)):
                event_owner = True
            elif (temp[i].fk_event.rsvp(self.request.user)):
                event_rsvp = True

            context['rsvp_list'][temp[i].id] = temp[i]
            context['rsvp_list'][temp[i].id].event_owner = event_owner 
            context['rsvp_list'][temp[i].id].event_rsvp = event_rsvp

        temp = UserTagAttribute.objects.filter(fk_user=t_user)
        context['tag_list'] = temp

        temp = Event.objects.filter(fk_event_poster_user=t_user)
        context['event_list'] = {}
#        import pdb;pdb.set_trace()

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

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(UserDetailView, self).dispatch(*args, **kwargs)

class UserImageListView(generic.ListView):
    template_name = 'basal/user_image_list.html'
    model = UserImage
    context_object_name = "user_image_list"

    def get_queryset(self):
        return UserImage.objects.filter(fk_user=self.request.user)

    def get_context_data(self, **kwargs):
        context = super(UserImageListView, self).get_context_data(**kwargs)
        context['current_path'] = self.request.get_full_path()
       # import pdb;pdb.set_trace()
        return context

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(UserImageListView, self).dispatch(*args, **kwargs)

class UserImageDetailView(generic.DetailView):
    template_name = 'basal/user_image_detail.html'
    model = UserImage

    def get_context_data(self, **kwargs):
        context = super(UserImageDetailView, self).get_context_data(**kwargs)
        if self.request.GET.get('back'):
            context['back'] = self.request.GET.get('back')
        return context

    @method_decorator(authorized_to_update_user_image_decorator)
    def dispatch(self, *args, **kwargs):
        return super(UserImageDetailView, self).dispatch(*args, **kwargs)

# work around solution for image upload, very insecure
class UserImageCreateAPIView(generic.CreateView):
    template_name = 'basal/user_image_create.html'
    model = UserImage

    def post(self, request, *args, **kwargs):
        try:
            user = CustomUser.objects.get(username=request.GET['username'])
#            import pdb;pdb.set_trace()
        except CustomUser.DoesNotExist:
            return HttpResponse(status=400)
        else:
            form = UserImage(fk_user=user, path=request.FILES['path'])
            form.save()
#            import pdb;pdb.set_trace()
#            return HttpResponse(status=201, content=form.path, content_type='text/plain')
            return HttpResponse(status=201, 
                                content=form.path.name, 
                                content_type='text/plain')

    def get_success_url(self):
        return self.request.POST.get('back')
    @method_decorator(csrf_exempt)
    def dispatch(self, *args, **kwargs):
        return super(UserImageCreateAPIView, self).dispatch(*args, **kwargs)

class UserImageCreateView(generic.CreateView):
    template_name = 'basal/user_image_create.html'
    model = UserImage

    form_class = UserImageForm

    def post(self, request, *args, **kwargs):
        self.object = None
        form = self.get_form(self.form_class)

        # let fk_user = current login user
        form.instance.fk_user = request.user

        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def get_success_url(self):
        return self.request.POST.get('back')

    def get_context_data(self, **kwargs):
        context = super(UserImageCreateView, self).get_context_data(**kwargs)
        if self.request.GET.get('back'):
            context['back'] = self.request.GET.get('back')
        return context

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(UserImageCreateView, self).dispatch(*args, **kwargs)

class UserImageUpdateView(generic.UpdateView):
    template_name = 'basal/user_image_update.html'
    model = UserImage
    form_class = UserImageForm
    context_object_name = 'user_image'

    def get_success_url(self):
        return self.request.POST.get('back')

    def get_context_data(self, **kwargs):
        context = super(UserImageUpdateView, self).get_context_data(**kwargs)
        if self.request.GET.get('back'):
            context['back'] = self.request.GET.get('back')
        return context

    @method_decorator(authorized_to_update_user_image_decorator)
    def dispatch(self, *args, **kwargs):
        return super(UserImageUpdateView, self).dispatch(*args, **kwargs)

class UserImageDeleteView(generic.DeleteView):
    template_name = 'basal/user_image_delete.html'
    model = UserImage
    context_object_name = 'user_image'

    def get_success_url(self):
        return self.request.POST.get('back')

    def get_context_data(self, **kwargs):
        context = super(UserImageDeleteView, self).get_context_data(**kwargs)
        if self.request.GET.get('back'):
            context['back'] = self.request.GET.get('back')
        return context

    @method_decorator(authorized_to_update_user_image_decorator)
    def dispatch(self, *args, **kwargs):
        return super(UserImageDeleteView, self).dispatch(*args, **kwargs)

@login_required
def user_tag_delete(request, pk):
    user_tag = UserTagAttribute.objects.get(pk=pk)
    user_tag.delete()

    return HttpResponseRedirect(reverse('basal:dashboard') + '#tags')

@login_required
def user_tag_create(request):
    temp = request.POST.get('tag_input')
#    import pdb;pdb.set_trace()
    if temp != '':
        user_tag = UserTagAttribute(fk_user=request.user, tag=temp)
        user_tag.save()

    return HttpResponseRedirect(reverse('basal:dashboard') + '#tags')
