from django.contrib import admin
from .models import Account

class AccountAdmin(admin.ModelAdmin):
    list_display = ['account_user_name', 'account_type', 'account_email',
                    'account_register_date']
    
admin.site.register(Account, AccountAdmin)
