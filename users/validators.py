import re

from django.core.exceptions import ValidationError

from core.consts import PASSWORDMINIMUMLENGTH


def minimum_length_validator(password):
    if len(password) < PASSWORDMINIMUMLENGTH:
        raise ValidationError(
            'Пароль должен содержать минимум'
            f'{PASSWORDMINIMUMLENGTH} символов')


def letter_password_validator(password):
    if not re.search(r'\d', password):
        raise ValidationError('Пароль должен содержать хотя бы одну цифру')


def phone_number_validator(phone_number):
    if not re.search(r'(^8\d{10}$)|(^\+7\d{10}$)', phone_number):
        raise ValidationError('Номер телефона введен неправильно')
