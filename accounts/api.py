from tastypie.resources import ModelResource

from tastypie import fields
from tastypie.constants import ALL

from models import Account

class AccountResource(ModelResource):
    class Meta:
        queryset = Account.objects.all()
        resource_name = 'account'
        excludes = ['account_password', 'account_type',
                    'account_register_date', 'account_image']
        filtering = { 'account_user_name': ALL }
