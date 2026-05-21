from core.avatar_generator import generate_avatar
from django.contrib.auth.models import BaseUserManager


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
