from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager

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

    username = models.CharField(max_length=20, unique=True)
    user_first_name = models.CharField(max_length=50, blank=True)
    user_last_name = models.CharField(max_length=50, blank=True)
    email = models.EmailField(max_length=100, unique=True)
    date_joined = models.DateTimeField(default=timezone.now)
    user_gender = models.CharField(max_length=10,
                                   choices=USER_GENDER_CHOICES,
                                   blank=True)
    user_description = models.TextField(blank=True)
    user_nickname = models.CharField(max_length=50, blank=True)

    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    objects = CustomUserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    class Meta:
        verbose_name = 'user'
        verbose_name_plural = 'users'

    def get_absolute_url(self):
        return "/users/%s/" % (self.username)

    def get_full_name(self):
        return '%s %s' % (self.user_first_name, self.user_last_name)

    def get_short_name(self):
        return self.user_first_name
