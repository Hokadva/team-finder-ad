from django.urls import path

from .views import (FavoriteProjectListView, ProjectCreateView,
                    ProjectDetailView, ProjectListView, ProjectUpdateView,
                    project_close, toggle_favorite, toggle_participate)

app_name = 'projects'

urlpatterns = [
    path(
        'list/', ProjectListView.as_view(),
        name='project_list'),
    path(
        '<int:pk>/edit/', ProjectUpdateView.as_view(),
        name='project_update'),
    path(
        '<int:pk>/toggle-participate/', toggle_participate,
        name='toggle_participate'),
    path(
        '<int:pk>/complete/', project_close, name='project_close'),
    path(
        '<int:pk>/toggle-favorite/', toggle_favorite,
        name='toggle_favorite'),
    path(
        '<int:pk>/', ProjectDetailView.as_view(),
        name='project_detail'),
    path(
        'create-project/', ProjectCreateView.as_view(),
        name='project_create'),
    path(
        'favorites/', FavoriteProjectListView.as_view(),
        name='favorite_projects')
]
