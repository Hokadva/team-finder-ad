import re

from django.core.exceptions import ValidationError


def github_url_validator(url):
    if not re.search(r'^https://github', url):
        raise ValidationError('Ссылка не ведет на github')
