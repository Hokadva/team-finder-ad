import subprocess
import sys
from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse
from .models import Project

User = get_user_model()


class LintersTestCase(TestCase):
    def test_flake8_compliance(self):
        result = subprocess.run(
            [
                sys.executable, '-m', 'flake8', '.',
                '--exclude=venv,*/migrations/*,core/settings.py',
                '--max-line-length=79',
                '--ignore=D100,D101,D103,D102,D106,D105,D104,F841,F401'],
            capture_output=True,
            text=True
        )
        self.assertEqual(
            result.returncode, 0,
            msg=f"Flake8 обнаружил ошибки стиля кода:\n{result.stdout}"
        )
