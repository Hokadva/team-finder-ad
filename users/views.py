from django.contrib import messages
from django.contrib.auth import login, logout, update_session_auth_hash
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import PasswordChangeView
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views.generic import DetailView
from django_filters.views import FilterView

from core.decorators import login_required_message

from .filters import UserFilter
from .forms import (ChangePasswordForm, ChangeProfileForm, LoginForm,
                    RegisterForm)
from .models import User


def register_user(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('/projects/list/')
    else:
        form = RegisterForm()

    return render(request, 'users/register.html', {'form': form})


def login_user(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            user = form.user
            login(request, user)
            return redirect('/projects/list')
    else:
        form = LoginForm()
    return render(request, 'users/login.html', {'form': form})


def logout_user(request):
    logout(request)
    return redirect('/projects/list/')


class UserPasswordChangeView(LoginRequiredMixin, PasswordChangeView):
    template_name = 'users/change_password.html'
    form_class = ChangePasswordForm

    def get_success_url(self):
        return reverse_lazy('users:profile',
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
        context['is_owner'] = self.request.user.is_authenticated and\
            self.request.user.pk == self.object.pk
        return context


@login_required_message()
def profile_edit(request):
    if request.method == 'POST':
        form = ChangeProfileForm(
            request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('users:profile', pk=request.user.pk)
    else:
        form = ChangeProfileForm(instance=request.user)
    return render(request, 'users/edit_profile.html', {'form': form})


class UserListView(FilterView):
    model = User
    template_name = 'users/participants.html'
    context_object_name = 'participants'
    filterset_class = UserFilter
    paginate_by = 12
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
