from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from tastypie.models import create_api_key

class CustomUserManager(BaseUserManager):
    def _create_user(self, user_name, password, is_staff, 
                     is_superuser, **extra_fields):
        """
        creates and saves a CustomUser with the given informations
        """
        now = timezone.now()

        if not user_name:
            raise ValueError('The given username must be set')

        user = self.model(user_name=user_name,
                          is_staff=is_staff, is_active=True,
                          is_superuser=is_superuser,
                          last_login=now, date_joined=now,
                          **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, user_name, password=None,
                    **extra_fields):
        return self._create_user(user_name, password,
                                 False, False, **extra_fields)

    def create_superuser(self, user_name, password,
                         **extra_fields):
        return self._create_user(user_name, password,
                                 True, True, **extra_fields)

class CustomUser(AbstractBaseUser, PermissionsMixin):
    USER_GENDER_CHOICES = (
            ('male', 'male'),
            ('female', 'female'),
    )
    
    user_name = models.CharField(max_length=255, unique=True)
#    user_email = models.EmailField(max_length=255, blank=True)
    user_first_name = models.CharField(max_length=255, blank=True)
    user_last_name = models.CharField(max_length=255, blank=True)
#    user_gender = models.CharField(max_length=10,
#                                   choices=USER_GENDER_CHOICES,
#                                   blank=True)
#    user_description = models.TextField(blank=True)
#    user_nickname = models.CharField(blank=True, max_length=255)
    date_joined = models.DateTimeField(default=timezone.now)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    objects = CustomUserManager()

    USERNAME_FIELD = 'user_name'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

#    def get_absolute_url(self):
#        return '/users/%s/' % (self.user_name)
#
    def get_full_name(self):
        return '%s %s' % (self.user_first_name, self.user_last_name)

    def get_short_name(self):
        return self.user_first_name
#
#    def email_user(self, subject, message, from_email=None, **kwargs):
#        """
#        Sends an email to this user
#        """
#        send_mail(subject, message, from_email, [self.user_email], **kwargs)

class Address(models.Model):
    address_title = models.CharField(max_length=100)
    address_detail = models.TextField()
    address_postal_code = models.CharField(blank=True, max_length=255)
    address_city = models.CharField(blank=True, max_length=255)
    address_region = models.CharField(blank=True, max_length=255)
    address_country = models.CharField(blank=True, 
                                       max_length=255, 
                                       default='Canada')

    def __unicode__(self):
        return self.address_title

#class UserAddressAttribute(models.Model):
#    fk_user_id = models.ForeignKey(CustomUser)
#    fk_address_id = models.ForeignKey(Address)
#
#    def __unicode__(self):
#        return "%s - %s" % (self.fk_user_id, self.fk_address_id)
#
#class UserFriendAttribute(models.Model):
#    fk_friend_a_user = models.ForeignKey(CustomUser, related_name='friend_a')
#    fk_friend_b_user = models.ForeignKey(CustomUser, related_name='friend_b')
#
#    def __unicode__(self):
#        return "%s - %s" % (self.fk_friend_a_user, self.fk_friend_b_user)

#def create_user_profile(sender, **kwargs):
#    """
#    A Signal for hooking up automatic ''UserProfile'' creation.
#    """
#    if kwargs.get('created') is True:
#        import pdb;pdb.set_trace()
        #UserProfile.objects.create(user=kwargs.get('instance'))

models.signals.post_save.connect(create_api_key, sender=CustomUser)
#models.signals.post_save.connect(create_user_profile, sender=User)


