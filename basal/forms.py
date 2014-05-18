from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import *
from django import forms

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

class UserUpdateForm(forms.ModelForm):
    """
    Form use for user_update page
    """

    CHOICES=[('male','male'),('female','female')]
    user_gender = forms.ChoiceField(choices=CHOICES, widget=forms.RadioSelect)
    class Meta:
        model = CustomUser
        exclude = ['password', 'last_login', 'is_superuser', 
                   'last_login', 'date_joined', 'groups', 
                   'is_staff', 'is_active', 'user_permissions']

class AddressForm(forms.ModelForm):
    class Meta:
        model = Address
        exclude = ['fk_user']

class UserImageForm(forms.ModelForm):
    class Meta:
        model = UserImage
        exclude = ['fk_user']
