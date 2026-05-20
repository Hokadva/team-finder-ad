from functools import wraps

from django.contrib import messages
from django.shortcuts import redirect


def login_required_message(
        message='Необходимо войти в систему или зарегистрироваться',
        redirect_to='users:login'):
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            if not request.user.is_authenticated:
                messages.error(request, message)
                return redirect(redirect_to)
            return view_func(request, *args, **kwargs)
        return wrapper
    return decorator
