from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .models import User


@admin.register(User)
class MyUserAdmin(BaseUserAdmin):
    ordering = ('email', 'name')
    list_display = ('email', 'phone', 'is_staff', 'is_active')
    list_filter = ('is_staff', 'is_active')
    search_fields = ('email', 'phone')
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Права доступа', {'fields': ('is_staff', 'is_active', 'groups',
                                      'user_permissions')}),
        ('Дополнительная информация', {'fields': ('avatar', 'phone')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'phone', 'password'),
        }),
    )
