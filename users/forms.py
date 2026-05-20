from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError

from core.avatar_generator import generate_avatar
from core.validators import github_url_validator

from .models import User
from .validators import (letter_password_validator, minimum_length_validator,
                         phone_number_validator)


class RegisterForm(forms.ModelForm):
    password = forms.CharField(
        label='Пароль',
        widget=forms.PasswordInput()
    )

    class Meta:
        model = User
        fields = ['name', 'surname', 'email']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
            generate_avatar(user)
            user.save()
        return user

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise ValidationError('Пользователь с таким email уже существует')
        return email

    def clean_password(self):
        password = self.cleaned_data.get('password')

        if password:
            minimum_length_validator(password)
            letter_password_validator(password)

            try:
                validate_password(password, user=None)
            except ValidationError as e:
                raise ValidationError(e.messages)
        return password


class ChangePasswordForm(PasswordChangeForm):
    old_password = forms.CharField(
        label='Старый пароль',
        widget=forms.PasswordInput()
    )

    new_password1 = forms.CharField(
        label='Новый пароль',
        widget=forms.PasswordInput()
    )

    new_password2 = forms.CharField(
        label='Подтверждение нового пароля',
        widget=forms.PasswordInput()
    )

    def clean_new_password1(self):
        password = self.cleaned_data.get('new_password1')
        if password:
            try:
                validate_password(password, self.user)
            except ValidationError as error:
                raise forms.ValidationError(error.messages)
        return password

    def clean(self):
        cleaned_data = super().clean()
        return cleaned_data


class LoginForm(forms.Form):
    email = forms.EmailField(
        label='Адрес электронной почты',
        widget=forms.EmailInput()
    )
    password = forms.CharField(
        label='Пароль',
        widget=forms.PasswordInput()
    )

    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get('email')
        password = cleaned_data.get('password')

        if email and password:
            user = authenticate(email=email, password=password)
            if not user:
                raise forms.ValidationError(
                    'Неверный адрес электронной почты или пароль')
            self.user = user
        return cleaned_data


class ChangeProfileForm(forms.ModelForm):
    phone = forms.CharField(
        validators=[phone_number_validator], required=False)
    github_url = forms.URLField(
        validators=[github_url_validator], required=False)

    class Meta:
        model = User
        fields = ['name', 'surname', 'avatar', 'about', 'phone', 'github_url']

    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        if phone and phone[0] == '+':
            phone = '8' + phone[2:]
        return phone
