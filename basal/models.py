from django.db import models
from django.contrib.auth.models import User
from tastypie.models import create_api_key

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

class UserAddressAttribute(models.Model):
    fk_user_id = models.ForeignKey(User)
    fk_address_id = models.ForeignKey(Address)

    def __unicode__(self):
        return "%s - %s" % (self.fk_user_id, self.fk_address_id)

class UserProfile(models.Model):
    USER_GENDER_CHOICES = (
            ('male', 'male'),
            ('female', 'female'),
            )

    user = models.OneToOneField(User, related_name='profile')
    user_gender = models.CharField(max_length=10,
            choices=USER_GENDER_CHOICES,
            blank=True)
    user_description = models.TextField(blank=True)
    user_nickname = models.CharField(blank=True, max_length=255)

    def __unicode__(self):
        return self.user.username

class UserFriendAttribute(models.Model):
    fk_friend_a_user = models.ForeignKey(User, related_name='friend_a')
    fk_friend_b_user = models.ForeignKey(User, related_name='friend_b')

    def __unicode__(self):
        return "%s - %s" % (self.fk_friend_a_user, self.fk_friend_b_user)

#def create_user_profile(sender, **kwargs):
#    """
#    A Signal for hooking up automatic ''UserProfile'' creation.
#    """
#    if kwargs.get('created') is True:
#        import pdb;pdb.set_trace()
        #UserProfile.objects.create(user=kwargs.get('instance'))

models.signals.post_save.connect(create_api_key, sender=User)
#models.signals.post_save.connect(create_user_profile, sender=User)


