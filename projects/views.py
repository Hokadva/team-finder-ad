from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.views.generic import CreateView, DetailView, ListView, UpdateView

from core.consts import STATUS_CHOICES
from core.decorators import login_required_message
from core.mixins import ProjectDeterminateContext

from .forms import ProjectForm
from .models import Project


class ProjectListView(ListView):
    model = Project
    template_name = 'projects/project_list.html'
    paginate_by = 12
    context_object_name = 'projects'
    form_class = ProjectForm
    ordering = ['-created_at']


class ProjectDetailView(DetailView):
    model = Project
    template_name = 'projects/project-details.html'
    form_class = ProjectForm


class ProjectCreateView(ProjectDeterminateContext, CreateView):
    model = Project
    template_name = 'projects/create-project.html'
    form_class = ProjectForm

    def form_valid(self, form):
        project = form.save(commit=False)
        project.owner = self.request.user
        project.created_at = timezone.now()
        project.save()
        project.participants.add(self.request.user)
        return super().form_valid(form)


class ProjectUpdateView(ProjectDeterminateContext, UpdateView):
    model = Project
    template_name = 'projects/create-project.html'
    form_class = ProjectForm

    def dispatch(self, request, *args, **kwargs):
        project = self.get_object()
        if project.owner != request.user:
            raise PermissionDenied('Вы не являетесь автором этого проекта')
        return super().dispatch(request, *args, **kwargs)


@login_required_message()
def toggle_participate(request, pk):
    if request.method == 'POST':
        project = get_object_or_404(Project, pk=pk)
        if project.status == STATUS_CHOICES[1][0]:
            return JsonResponse(
                {'status': 'error', 'message': 'Проект закрыт'}, status=400)
        if request.user == project.owner:
            return JsonResponse({'status': 'error'}, status=400)
        is_participant = project.participants.filter(id=request.user.id
                                                     ).exists()
        if is_participant:
            project.participants.remove(request.user)
            is_participant = False
        else:
            project.participants.add(request.user)
            is_participant = True
        return JsonResponse({'status': 'ok',
                             'participant': is_participant,
                             'participants_count':
                             project.participants.count()})


@login_required_message()
def project_close(request, pk):
    if request.method == 'POST':
        project = get_object_or_404(Project, pk=pk)
        if project.owner != request.user:
            return JsonResponse({'status': 'error'}, status=403)
        if project.status in STATUS_CHOICES[1]:
            return JsonResponse({'status': 'error'}, status=400)
        project.status = STATUS_CHOICES[1][0]
        project.save()
        return JsonResponse({
            'status': 'ok', 'project_status': STATUS_CHOICES[1][0]})


class FavoriteProjectListView(ProjectListView, LoginRequiredMixin):
    template_name = 'projects/favorite_projects.html'

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(interested_users=self.request.user)


@login_required_message()
def toggle_favorite(request, pk):
    if request.method == 'POST':
        project = get_object_or_404(Project, pk=pk)
        is_favorite = project.interested_users.filter(id=request.user.id
                                                      ).exists()
        if is_favorite:
            project.interested_users.remove(request.user)
            is_favorite = False
        else:
            project.interested_users.add(request.user)
            is_favorite = True
        return JsonResponse({'status': 'ok',
                             'participant': is_favorite,
                             'participants_count':
                             project.participants.count()})
