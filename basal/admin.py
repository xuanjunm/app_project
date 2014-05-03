from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import *
from .forms import *

class CustomUserAdmin(UserAdmin):
    # The forms to add and change user instances

    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference the removed 'username' field
    fieldsets = (
        (None, {
            'fields': ('username', 'email', 'password')
        }),
        ('Personal info', {
            'fields': ('user_first_name', 'user_last_name', 'user_gender', 
                       'user_description', 'user_nickname', 'fk_user_image',
                       'fk_user_background_image')
        }),
        ('Permissions', {
            'fields': ('is_active', 'is_staff', 'is_superuser',
                       'groups', 'user_permissions')
        }),
        ('Important dates', {
            'fields': ('last_login', 'date_joined')
        }),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2')}
        ),
    )

    form = CustomUserChangeForm
    add_form = CustomUserCreationForm
    list_display = ('username', 'email', 'user_first_name', 
                    'user_last_name', 'is_staff')
    search_fields = ('username', 'email', 'user_first_name', 
                     'user_last_name')
    ordering = ('username',)

admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Address)
admin.site.register(UserImage)
