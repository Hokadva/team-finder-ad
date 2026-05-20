from django.db import models
from django.urls import reverse

from core.consts import STATUS_CHOICES
from users.models import User


class Project(models.Model):
    name = models.CharField(max_length=200, verbose_name='название проекта')
    description = models.TextField(blank=True, verbose_name='описание проекта')
    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='owned_projects',
        verbose_name='автор проекта'
    )
    created_at = models.DateTimeField(verbose_name='дата создания проекта')
    github_url = models.URLField(blank=True, verbose_name='ссылка на Github')
    status = models.CharField(
        max_length=6,
        choices=STATUS_CHOICES,
        default='open',
        verbose_name='статус проекта'
    )
    participants = models.ManyToManyField(
        User,
        blank=True,
        related_name='participated_projects',
        verbose_name='участники проекта'
    )

    class Meta:
        verbose_name = 'Проект'
        verbose_name_plural = 'Проекты'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('project_detail', args=[self.id])
