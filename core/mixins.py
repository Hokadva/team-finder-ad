from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.shortcuts import redirect


class ProjectDeterminateContext:
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_edit'] = 'edit' in self.request.path
        return context

    def form_valid(self, form):
        project = form.save()
        return redirect('projects:project_detail', pk=project.pk)


class OwnerRequiredMixin:
    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        if obj.owner != request.user:
            raise PermissionDenied('Вы не являетесь автором этого проекта')
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        project = form.save()
        return redirect('projects:project_detail', pk=project.pk)
