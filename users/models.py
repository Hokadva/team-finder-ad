from django.contrib.auth.models import AbstractUser
from django.db import models
from users.managers import UserManager
from core.consts import (
    NAMEMAXLENGTH, SURNAMEMAXLENGTH, PHONEMAXLENGTH, ABOUTMAXLENGTH
)


class User(AbstractUser):
    email = models.EmailField(
        unique=True, verbose_name='адрес электронной почты')
    name = models.CharField(
        max_length=NAMEMAXLENGTH, verbose_name='имя пользователя')
    surname = models.CharField(
        max_length=SURNAMEMAXLENGTH, verbose_name='фамилия пользователя')
    avatar = models.ImageField(
        blank=True, null=True, upload_to='avatars/',
        verbose_name='аватарка пользователя')
    phone = models.CharField(
        max_length=PHONEMAXLENGTH, null=True, unique=True,
        verbose_name='номер телефона')
    github_url = models.URLField(
        blank=True, verbose_name='ссылка на Github')
    about = models.TextField(
        max_length=ABOUTMAXLENGTH, blank=True,
        verbose_name='описание профиля')
    is_active = models.BooleanField(
        default=True, verbose_name='активный пользователь')
    is_staff = models.BooleanField(
        default=False, verbose_name='администратор')

    first_name = None
    last_name = None
    username = None
    is_superuser = None
    last_login = None
    date_joined = None

    favorites = models.ManyToManyField(
        'projects.Project',
        related_name='interested_users',
        blank=True,
        verbose_name='избранные проекты'
    )

    objects = UserManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name', 'surname']

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def has_perm(self, perm, obj=None):
        return self.is_staff

    def has_module_perms(self, app_label):
        return self.is_staff
