from django.db import models
from django.contrib.auth.models import User
from tastypie.models import create_api_key

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

class UserFriendAttribute(models.Model):
    fk_friend_a_user = models.ForeignKey(User, related_name='friend_a')
    fk_friend_b_user = models.ForeignKey(User, related_name='friend_b')

def create_user_profile(sender, **kwargs):
    """
    A Signal for hooking up automatic ''UserProfile'' creation.
    """
    if kwargs.get('created') is True:
        UserProfile.objects.create(user=kwargs.get('instance'))

models.signals.post_save.connect(create_api_key, sender=User)
models.signals.post_save.connect(create_user_profile, sender=User)


