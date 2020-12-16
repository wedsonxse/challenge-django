
import uuid
from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser
from django.utils import timezone

class UserManager(BaseUserManager):
    '''
    creating a manager for a custom user model
    https://docs.djangoproject.com/en/3.0/topics/auth/customizing/#writing-a-manager-for-a-custom-user-model
    https://docs.djangoproject.com/en/3.0/topics/auth/customizing/#a-full-example
    '''
    def create_user(self, e_mail, password):
        """
        Create and return a `User` with an email, username and password.
        """
        if not e_mail:
            raise ValueError('Users Must Have an email address')

        user = self.model(
            e_mail=e_mail,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, e_mail, password):
        """
        Create and return a `User` with superuser (admin) permissions.
        """
        if password is None:
            raise TypeError('Superusers must have a password.')

        user = self.create_user(e_mail, password)
        user.is_superuser = True
        user.is_staff = True
        user.save()

        return user


class User(AbstractBaseUser):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    e_mail = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True
        )
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)
    USERNAME_FIELD = 'e_mail'
    REQUIRED_FIELDS = []

    # Tells Django that the UserManager class defined above should manage
    # objects of this type.
    objects = UserManager()

    def __str__(self):
        return self.e_mail

    class Meta:
        '''
        set table name in db
        '''
        db_table = "login"