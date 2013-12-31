from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    USER_GENDER_CHOICES = (
        ('male', 'male'),
        ('female', 'female'),
    )

    user = models.OneToOneField(User)
    user_gender = models.CharField(max_length=10,
                                   choices=USER_GENDER_CHOICES)
    user_description = models.TextField(blank=True)
    user_nickname = models.CharField(blank=True, max_length=255)

class UserFriendAttribute(models.Model):
    fk_friend_a_user = models.ForeignKey(User, related_name='friend_a')
    fk_friend_b_user = models.ForeignKey(User, related_name='friend_b')
