from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager

from django.utils.translation import ugettext_lazy as _
from tastypie.models import create_api_key

class CustomUserManager(BaseUserManager):
    def _create_user(self, username, email, password, 
                     is_staff, is_superuser, **extra_fields): 
        now = timezone.now()
        if not username:
            raise ValueError('The given username must be set')
        email = self.normalize_email(email)
        user = self.model(username=username, email=email,
                            is_staff=is_staff, is_active=True,
                            is_superuser=is_superuser, last_login=now,
                            date_joined=now, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, username, email=None, password=None, **extra_fields):
        return self._create_user(username, email, password, False, False,
                                 **extra_fields)

    def create_superuser(self, username, email, password, **extra_fields):
        return self._create_user(username, email, password, True, True, 
                                    **extra_fields)

class CustomUser(AbstractBaseUser, PermissionsMixin):
    USER_GENDER_CHOICES = (
        ('male', 'male'),
        ('female', 'female'),
    )

    username = models.CharField(max_length=255, unique=True)
    user_first_name = models.CharField(max_length=255, blank=True)
    user_last_name = models.CharField(max_length=255, blank=True)
    email = models.EmailField(max_length=255, unique=True)
    date_joined = models.DateTimeField(default=timezone.now)
    user_gender = models.CharField(max_length=255,
                                   choices=USER_GENDER_CHOICES,
                                   blank=True)
    user_description = models.TextField(blank=True)
    user_nickname = models.CharField(max_length=255, blank=True)
    fk_user_background_image = models.ForeignKey('UserImage', blank=True, null=True, related_name='user_background_image')
    fk_user_image = models.ForeignKey('UserImage', blank=True, null=True, related_name='user_image')
    # UserImage is between quote because of circular reference

    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    objects = CustomUserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def get_absolute_url(self):
        return '/users/%s/' % (self.username)

    def get_full_name(self):
        return u'%s %s' % (self.user_first_name, self.user_last_name)

    def get_short_name(self):
        return u'%s' % self.user_first_name

    def __unicode__(self):
        return u'%s' % self.username 

class UserImage(models.Model):
    path = models.ImageField(upload_to='user_image', 
                             help_text='help text',      
                             blank=True)
    fk_user = models.ForeignKey(CustomUser)

    def is_owner(self, user):
        return self.fk_user == user

    def __unicode__(self):
        return u'%s' % self.path 

class Address(models.Model):
    address_title = models.CharField(max_length=255)
    address_detail = models.TextField()
    address_postal_code = models.CharField(blank=True, max_length=255)
    address_city = models.CharField(blank=True, max_length=255)
    address_region = models.CharField(blank=True, max_length=255)
    address_country = models.CharField(blank=True, 
                                       max_length=255, 
                                       default='Canada')
    fk_user = models.ForeignKey(CustomUser)

    def is_owner(self, user):
        return self.fk_user == user

    def __unicode__(self):
        return u'%s - %s' % (self.fk_user, self.address_title)

class UserFriendAttribute(models.Model):
    fk_friend_a_user = models.ForeignKey(CustomUser, related_name='friend_a')
    fk_friend_b_user = models.ForeignKey(CustomUser, related_name='friend_b')

    def __unicode__(self):
        return '%s - %s' % (self.fk_friend_a_user, self.fk_friend_b_user)
                                        
#def create_user_image(sender, **kwargs):        
#    """
#    A Signal for hooking up automatic 'UserImage' creation.
#    """
#    if kwargs.get('created') is True:
#        import pdb;pdb.set_trace()
#        UserImage.objects.create()

models.signals.post_save.connect(create_api_key, sender=CustomUser)
#models.signals.post_save.connect(create_user_image, sender=CustomUser)
