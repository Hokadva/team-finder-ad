from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect


class ProjectDeterminateContext(LoginRequiredMixin):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_edit'] = 'edit' in self.request.path
        return context

    def form_valid(self, form):
        project = form.save()
        return redirect('projects:project_detail', pk=project.pk)
