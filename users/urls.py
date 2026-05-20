from django.urls import path

from .views import (UserListView, UserPasswordChangeView, UserProfileView,
                    login_user, logout_user, profile_edit, register_user)

app_name = 'users'

urlpatterns = [
    path('<int:pk>/', UserProfileView.as_view(), name='profile'),
    path('register/', register_user, name='register'),
    path('login/', login_user, name='login'),
    path('logout/', logout_user, name='logout'),
    path('change-password/', UserPasswordChangeView.as_view(),
         name='change-password'),
    path('edit-profile/', profile_edit, name='edit-profile'),
    path('list/', UserListView.as_view(), name='user-list')
]
