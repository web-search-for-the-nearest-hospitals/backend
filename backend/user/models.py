# myapp/models.py
from django.db import models
from django.contrib.auth.models import AbstractUser


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
        help_text="Укажите email пользователя",
    )
    role = models.CharField(
        max_length=9,
        choices=Roles.choices,
        default=Roles.USER,
        verbose_name="роль",
        help_text="Выберите роль (администратор/доктор/пациент)",
    )
    first_name = models.CharField(
        verbose_name="имя",
        max_length=150,
        null=True,
    )
    last_name = models.CharField(
        verbose_name="фамилия",
        max_length=150,
        null=True,
    )
    phone = models.CharField(
        verbose_name="номер телефона", max_length=15, blank=True, null=True
    )
    date_of_birth = models.DateField(
        verbose_name="дата рождения", blank=True, null=True
    )

    def __str__(self):
        return self.email

    @property
    def is_admin(self):
        return self.is_staff or self.role == self.Roles.ADMIN

    @property
    def is_moderator(self):
        return self.role == self.Roles.MODERATOR