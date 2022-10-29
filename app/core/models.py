"""
Database models.
"""

from django.conf import settings
from django.utils.translation import gettext_lazy as _
from django.core.validators import (
    MinValueValidator,
    MaxValueValidator,
    MinLengthValidator
)
from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)


class UserManager(BaseUserManager):
    """Manager for users."""

    def create_user(self, email, password=None, **extra_fields):
        """Create, save and return a new user."""
        if not email:
            raise ValueError('User must have an email address.')
        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password):
        """Create and return a new superuser."""
        user = self.create_user(email, password)
        user.is_staff = True
        user.is_superuser = True

        user.save(using=self._db)

        return user


class User(AbstractBaseUser, PermissionsMixin):
    """User in the system."""
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'


class Drone(models.Model):
    """Drone object."""

    class DroneModel(models.IntegerChoices):
        LIGHTWEIGHT = 0, _('Lightweight')
        MIDDLEWEIGHT = 1, _('Middleweight')
        CRUISERWEIGHT = 2, _('Cruiserweight')
        HEAVYWEIGHT = 3, _('Heavyweight')

    class DroneState(models.IntegerChoices):
        IDLE = 0, _('Idle')
        LOADING = 1, _('Loading')
        LOADED = 2, _('Loaded')
        DELIVERING = 3, _('Delivering')
        DELIVERED = 4, _('Delivered')
        RETURNING = 5, _('Returning')

    def get_drone_model(self):
        """Get value from choices of drone model enum."""
        return self.DroneModel(self.model)

    def get_drone_state(self):
        """Get value from choices of drone state enum."""
        return self.DroneState(self.model)

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )

    serial_number = models.CharField(
        max_length=100,
        unique=True,
        validators=[
            MinLengthValidator(5)
        ]
        )

    drone_model = models.IntegerField(
        default=DroneModel.LIGHTWEIGHT,
        choices=DroneModel.choices,
        )

    weight_limit = models.IntegerField(
        default=500,
        validators=[
            MaxValueValidator(500),
            MinValueValidator(1)
        ]
        )

    battery = models.IntegerField(
        default=100,
        validators=[
            MaxValueValidator(100),
            MinValueValidator(0)
        ],
        )

    state = models.IntegerField(
        default=DroneState.IDLE,
        choices=DroneState.choices,
    )

    def __str__(self):
        return self.serial_number
