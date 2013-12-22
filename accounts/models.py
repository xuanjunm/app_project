from django.db import models

class Account(models.Model):
    ACCOUNT_TYPE_CHOICES = (
        ('regular', 'regular'),
        ('seller', 'seller'),
        ('admin', 'admin'),
        ('premium', 'premium'),
    )
    account_user_name = models.CharField(max_length=255)
    account_type = models.CharField(max_length=13,
                                    choices=ACCOUNT_TYPE_CHOICES,
                                    default='regular')
    account_password = models.CharField(max_length=255)
    account_email = models.CharField(blank=True, max_length=255)
    account_image = models.CharField(blank=True, max_length=255)
    account_register_date = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return self.account_user_name
