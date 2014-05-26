from django.contrib.auth.forms import UserCreationForm, UserChangeForm, AuthenticationForm
from .models import *
from django import forms

class metaForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(metaForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'

class CustomUserCreationForm(UserCreationForm):
    """
    A form that creates a user, with no privileges, from the given email and
    password.
    """
    def clean_username(self):
        username = self.cleaned_data["username"]
        try:
            CustomUser._default_manager.get(username=username)
        except CustomUser.DoesNotExist:
            return username

        raise forms.ValidationError(
            self.error_messages['duplicate_username'],
            code='duplicate_username',
        )
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super(CustomUserCreationForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'

class MyAuthenticationForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super(MyAuthenticationForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'

class CustomUserChangeForm(UserChangeForm):
    """
    A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    password hash display field.
    """

    def __init__(self, *args, **kargs):
        super(CustomUserChangeForm, self).__init__(*args, **kargs)

    class Meta:
        model = CustomUser

class UserUpdateForm(metaForm):
    """
    Form use for user_update page
    """

    CHOICES=[('male','male'),('female','female')]
    user_gender = forms.ChoiceField(choices=CHOICES, widget=forms.RadioSelect, required=False)

    class Meta:
        model = CustomUser
        exclude = ['password', 'last_login', 'is_superuser', 
                   'last_login', 'date_joined', 'groups', 
                   'is_staff', 'is_active', 'user_permissions']

    def __init__(self, *args, **kwargs):
        '''
        to remove the selected box around options
        '''
        super(UserUpdateForm, self).__init__(*args, **kwargs)
        self.fields['user_gender'].widget.attrs['class'] = ''

class AddressForm(metaForm):
    class Meta:
        model = Address
        exclude = ['fk_user']

class UserImageForm(forms.ModelForm):
    class Meta:
        model = UserImage
        exclude = ['fk_user']

class ContactView(generic.FormView):
    template_name = 'basal/contact.html'
    form_class = EmailForm

    def get_success_url(self):
        return reverse('basal:main')

    def form_valid(self, form):
        subject = form.cleaned_data['subject']
        sender = form.cleaned_data['sender']
        message = form.cleaned_data['message'] + '\n\nfrom ' + sender
        # import pdb;pdb.set_trace()
        cc_myself = form.cleaned_data['cc_myself']
        
        recipients = ['sillygrubs@gmail.com']
        if cc_myself:
            recipients.append(sender)
                                                                                                        send_mail(subject, message, sender, recipients)
        return super(ContactView, self).form_valid(form)
