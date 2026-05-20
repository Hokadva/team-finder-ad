from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models

from core.avatar_generator import generate_avatar


class UserManager(BaseUserManager):
    def create_user(self, email, name, surname, password=None, **kwargs):
        if not email:
            raise ValueError('Email обязателен')
        if not name:
            raise ValueError('Имя обязательно')
        if not surname:
            raise ValueError('Фамилия обязательна')

        email = self.normalize_email(email)
        user = self.model(
            email=email,
            name=name,
            surname=surname,
            **kwargs
        )
        user.set_password(password)
        user.save(using=self._db)
        generate_avatar(user)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, name, surname, **kwargs):
        kwargs['is_staff'] = True

        return self.create_user(
            email=email,
            name=name,
            surname=surname,
            **kwargs
        )


class User(AbstractUser):
    email = models.EmailField(
        unique=True, verbose_name='адрес электронной почты')
    name = models.CharField(
        max_length=124, verbose_name='имя пользователя')
    surname = models.CharField(
        max_length=124, verbose_name='фамилия пользователя')
    avatar = models.ImageField(
        blank=True, null=True, upload_to='avatars/',
        verbose_name='аватарка пользователя')
    phone = models.CharField(
        max_length=12, null=True, unique=True, verbose_name='номер телефона')
    github_url = models.URLField(
        blank=True, verbose_name='ссылка на Github')
    about = models.TextField(
        max_length=256, blank=True, verbose_name='описание профиля')
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
