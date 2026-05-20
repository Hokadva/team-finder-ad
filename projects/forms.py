from django import forms

from core.validators import github_url_validator

from .models import Project


class ProjectForm(forms.ModelForm):
    github_url = forms.URLField(
        validators=[github_url_validator], required=False)

    class Meta:
        model = Project
        fields = ['name', 'description', 'github_url', 'status']
