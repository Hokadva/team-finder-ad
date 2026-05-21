from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.views.generic import CreateView, DetailView, ListView, UpdateView
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from http import HTTPStatus

from core.consts import (
    ProjectStatus, PROJECTLISTPAGINATENUM)
from core.mixins import ProjectDeterminateContext, OwnerRequiredMixin

from .forms import ProjectForm
from .models import Project


class ProjectListView(ListView):
    model = Project
    template_name = 'projects/project_list.html'
    paginate_by = PROJECTLISTPAGINATENUM
    context_object_name = 'projects'
    form_class = ProjectForm
    ordering = ['-created_at']


class ProjectDetailView(DetailView):
    model = Project
    template_name = 'projects/project-details.html'
    form_class = ProjectForm


class ProjectCreateView(LoginRequiredMixin, ProjectDeterminateContext,
                        CreateView):
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


class ProjectUpdateView(
        LoginRequiredMixin, OwnerRequiredMixin,
        ProjectDeterminateContext, UpdateView):
    model = Project
    template_name = 'projects/create-project.html'
    form_class = ProjectForm


@login_required
@require_http_methods(["POST"])
def toggle_participate(request, pk):
    project = get_object_or_404(Project, pk=pk)
    if project.status == ProjectStatus.CHOICES[1][0]:
        return JsonResponse(
            {'status': 'error', 'message': 'Проект закрыт'},
            status=HTTPStatus.BAD_REQUEST)
    if request.user == project.owner:
        return JsonResponse({'status': 'error'},
                            status=HTTPStatus.BAD_REQUEST)
    if (is_participant := project.participants.filter(id=request.user.id)
            .exists()):
        project.participants.remove(request.user)
    else:
        project.participants.add(request.user)
    return JsonResponse({'status': 'ok',
                         'participant': not is_participant,
                         'participants_count':
                         project.participants.count()})


@login_required
@require_http_methods(["POST"])
def project_close(request, pk):
    project = get_object_or_404(Project, pk=pk)
    if project.owner != request.user:
        return JsonResponse({'status': 'error'},
                            status=HTTPStatus.FORBIDDEN)
    if project.status in ProjectStatus.CHOICES[1]:
        return JsonResponse({'status': 'error'},
                            status=HTTPStatus.BAD_REQUEST)
    project.status = ProjectStatus.CHOICES[1][0]
    project.save()
    return JsonResponse({
        'status': 'ok',
        'project_status': ProjectStatus.CHOICES[1][0]})


class FavoriteProjectListView(LoginRequiredMixin, ProjectListView):
    template_name = 'projects/favorite_projects.html'

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(
            interested_users=self.request.user).select_related(
                'owner').prefetch_related('participants')


@login_required
@require_http_methods(["POST"])
def toggle_favorite(request, pk):
    project = get_object_or_404(Project, pk=pk)
    if (is_favorite := project.interested_users.filter(
       id=request.user.id).exists()):
        project.interested_users.remove(request.user)
    else:
        project.interested_users.add(request.user)
    return JsonResponse({'status': 'ok',
                         'participant': is_favorite,
                         'participants_count':
                         project.participants.count()})
