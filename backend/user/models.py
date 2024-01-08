from django.contrib.auth.models import AbstractUser
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.db import models


class User(AbstractUser):
    """
    Модель пользователя с дополнительной информацией
    """

    class Roles(models.TextChoices):
        ADMIN = "admin"
        MODERATOR = "moderator"
        USER = "user"

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ("username",)

    email = models.EmailField(
        db_index=True,
        unique=True,
        max_length=254,
        help_text="Email пользователя",
    )

    username = models.CharField(
        max_length=150, unique=False,
        validators=[UnicodeUsernameValidator()],
        verbose_name='Никнейм пользователя',
        blank=True,
        null=True
    )

    role = models.CharField(
        max_length=9,
        choices=Roles.choices,
        default=Roles.USER,
        verbose_name="роль",
        help_text="Роль пользователя (администратор/модератор/пользователь)",
    )
    first_name = models.CharField(
        verbose_name="Имя",
        max_length=150,
        null=True,
        blank=True,
        help_text="Имя пользователя"
    )
    last_name = models.CharField(
        verbose_name="Фамилия",
        max_length=150,
        null=True,
        blank=True,
        help_text="Фамилия пользователя"
    )

    third_name = models.CharField(
        verbose_name="Отчество",
        max_length=150,
        null=True,
        blank=True,
        help_text="Отчество пользователя"
    )

    phone = models.CharField(
        verbose_name="Номер телефона",
        max_length=20,
        blank=True,
        null=True,
        help_text="Номер телефона пользователя"
    )
    date_of_birth = models.DateField(
        verbose_name="Дата рождения",
        blank=True,
        null=True,
        help_text="Дата рождения пользователя"
    )

    def __str__(self):
        return self.email

    @property
    def is_admin(self):
        return self.is_staff or self.role == self.Roles.ADMIN

    @property
    def is_moderator(self):
        return self.role == self.Roles.MODERATOR
