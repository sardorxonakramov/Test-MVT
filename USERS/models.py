from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.utils import timezone
from django.core.validators import RegexValidator

from .managers import CustomUserManager


class CustomUser(AbstractBaseUser, PermissionsMixin):
    """Custom user model with email authentication and role-based access."""

    ROLE_CHOICES = (
        ("admin", "Admin"),
        ("teacher", "Teacher"),
        ("student", "Student"),
    )

    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30, blank=True, null=True)

    phone = models.CharField(
        max_length=13,
        unique=True,
        validators=[
            RegexValidator(
                regex=r"^\+998\d{9}$",
                message="Telefon raqam formati: +998901234567 bo'lishi kerak.",
            )
        ],
        help_text="Masalan: +998901234567",
    )

    role = models.CharField(
        max_length=10,
        choices=ROLE_CHOICES,
        default="student"
    )
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)

    objects = CustomUserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "phone"]

    def __str__(self):
        return f"{self.email} ({self.role})"

    @property
    def full_name(self):
        """Return the full name of the user."""
        if self.last_name:
            return f"{self.first_name} {self.last_name}"
        return self.first_name
