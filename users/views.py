from django.contrib import messages
from django.contrib.auth import login, logout, update_session_auth_hash
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import PasswordChangeView
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.views.generic import DetailView
from django_filters.views import FilterView

from .filters import UserFilter
from .forms import (ChangePasswordForm, ChangeProfileForm, LoginForm,
                    RegisterForm)
from .models import User
from core.consts import USERLISTPAGINATENUM


def register_user(request):
    form = RegisterForm(request.POST or None)
    if form.is_valid():
        user = form.save()
        login(request, user)
        return redirect('projects:project_list')

    return render(request, 'users/register.html', {'form': form})


def login_user(request):
    form = LoginForm(request.POST or None)
    if form.is_valid():
        user = form.user
        login(request, user)
        return redirect('projects:project_list')
    return render(request, 'users/login.html', {'form': form})


def logout_user(request):
    logout(request)
    return redirect('projects:project_list')


class UserPasswordChangeView(LoginRequiredMixin, PasswordChangeView):
    template_name = 'users/change_password.html'
    form_class = ChangePasswordForm

    def get_success_url(self):
        return reverse('users:profile',
                       kwargs={'pk': self.request.user.pk})

    def form_valid(self, form):
        response = super().form_valid(form)
        update_session_auth_hash(self.request, form.user)
        messages.success(self.request, 'Пароль успешно изменен!')
        return response

    def form_invalid(self, form):
        for field, errors in form.errors.items():
            for error in errors:
                messages.error(self.request, error)
        return super().form_invalid(form)


class UserProfileView(DetailView):
    model = User
    template_name = 'users/user-details.html'

    def get_object(self):
        return get_object_or_404(User, pk=self.kwargs['pk'])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user_projects'] = (self.object.owned_projects.
                                    all().order_by('-created_at'))
        context['is_owner'] = (self.request.user.is_authenticated and self
                               .request.user.pk == self.object.pk)
        return context


@login_required
def profile_edit(request):
    form = ChangeProfileForm(
        request.POST or None, request.FILES or None,
        instance=request.user or None)
    if form.is_valid():
        form.save()
        return redirect('users:profile', pk=request.user.pk)
    return render(request, 'users/edit_profile.html', {'form': form})


class UserListView(FilterView):
    model = User
    template_name = 'users/participants.html'
    context_object_name = 'participants'
    filterset_class = UserFilter
    paginate_by = USERLISTPAGINATENUM
    ordering = ['-id']

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.request.user.is_authenticated:
            queryset = queryset.exclude(id=self.request.user.id)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['active_filter'] = self.request.GET.get('filter')
        return context

    def get_filterset_kwargs(self, filterset_class):
        kwargs = super().get_filterset_kwargs(filterset_class)
        kwargs['request'] = self.request
        return kwargs
